from flask import Blueprint, request, jsonify, send_file

from src import celery_app
from src.blueprints.utils.api_key import require_api_key
from src.data_model.dataset import Dataset
from src.data_model.model import ModelTypes, Model, ModelStatus
from src.data_source.aws import retrieve_file_from_s3, FileType
from s0nar_analytics.analysis_module.src import analysis_module
from s0nar_analytics.data_models import extended_dataset

model_blueprint = Blueprint("model", __name__)


@model_blueprint.route('/s0nar/v1/anomalies/model', methods=['GET'])
def retrieve_all_models():
    """
    Create dataset
    ---
    responses:
      200:
        description: A single user item
    Retrieves all models, also, this list can be filter by several parameters, such as, status, type, dataset, etc.

    :return: list with all persisted models
    """
    filters = {}

    if request.get_json() is not None:
        if request.get_json().get('dataset'):
            filters['dataset'] = request.get_json().get('dataset')

        if request.get_json().get('status'):
            filters['status'] = request.get_json().get('status')

        if request.get_json().get('type'):
            filters['type'] = request.get_json().get('type')

        if request.get_json().get('target_feature'):
            filters['target_feature'] = request.get_json().get('target_feature')

        if request.get_json().get('hyper_parameters'):
            filters['hyper_parameters'] = request.get_json().get('hyper_parameters')

    response = [model.to_mongo().to_dict() for model in Model.find_all(filters)]
    return jsonify(response), 200


@model_blueprint.route('/s0nar/v1/anomalies/<dataset_id>/model', methods=['POST'])
@require_api_key
def create_model(dataset_id):
    """
    Create dataset
    ---
    parameters:
      - in: path
        name: dataset_id
        type: int
        required: true
    responses:
      200:
        description: A single user item
    Creates an entity which represents some model attached to certain dataset and with some of its features

    :return: model entity persisted on database
    """
    dataset = Dataset.find_one({'id': dataset_id})
    type = ModelTypes(request.get_json().get('type').upper())
    target_feature = request.get_json()['target_feature']
    index_feature = request.get_json()['index']
    index_schema = request.get_json()['index_schema']
    hyper_parameters = request.get_json().get('hyper_parameters', dict())

    model = Model(dataset=dataset,
                  type=type.value,
                  hyper_parameters=hyper_parameters,
                  target_feature=target_feature,
                  index_feature=index_feature,
                  index_schema=index_schema).create()

    return model.to_mongo().to_dict(), 200


@model_blueprint.route('/s0nar/v1/anomalies/model/<id>/details', methods=['GET'])
def retrieve_model(id):
    """
    Create dataset
    ---
    parameters:
      - in: path
        name: id
        type: int
        required: true
    responses:
      200:
        description: A single user item
    Retrieves model by its id

    :param id: uuid which represents the model

    :return: Dataset
    :raise 404: if there isn't any model with that id
    """
    return Model.find_one({'id': id}).to_mongo().to_dict(), 200


@model_blueprint.route('/s0nar/v1/anomalies/model/<id>/bin', methods=['GET'])
@require_api_key
def download_bin_model(id):
    """
    Create dataset
    ---
    parameters:
      - in: path
        name: id
        type: int
        required: true
    responses:
      200:
        description: A single user item
    Download the model persisted on Amazon's S3 Bucket, for both algorithms (ARIMA and LSTM)

    :param id: uuid which represents the model

    :return: Binary content, .pkl for Auto-Arima and .h5 for tf model of LSTM
    :raise 404: if there isn't any model with that id
    """
    model = Model.find_one({'id': id, 'status': ModelStatus.FINISHED.value})

    if model.type == ModelTypes.ARIMA.value:
        file_type = FileType.ARIMA_BIN
    elif model.type in [ModelTypes.LSTM_CPU.value, ModelTypes.LSTM_GPU.value]:
        file_type = FileType.TENSORFLOW_BIN
    else:
        raise Exception('Model type not found')
    local_path = retrieve_file_from_s3(model.bin_s3_uri, model.generate_name(), file_type)
    return send_file(local_path, attachment_filename=model.generate_name())


@model_blueprint.route('/s0nar/v1/anomalies/model/<id>/json', methods=['GET'])
@require_api_key
def download_json_model(id):
    """
    Create dataset
    ---
    parameters:
      - in: path
        name: id
        type: int
        required: true
    responses:
      200:
        description: A single user item
    Download related model information persisted on Amazon's S3 Bucket, for LSTM algorithms (hyperparams,
    neuron topology)

    :param id: uuid which represents the model

    :return: dict with all related information
    :raise 404: if there isn't any model with that id
    """
    model = Model.find_one({'id': id, 'status': ModelStatus.FINISHED.value})
    local_path = retrieve_file_from_s3(model.json_s3_uri, model.generate_name(), FileType.TENSORFLOW_JSON)
    return send_file(local_path, attachment_filename=model.generate_name())


@model_blueprint.route('/s0nar/v1/anomalies/model/<id>', methods=['PATCH'])
@require_api_key
def update_model(id):
    """
    Create dataset
    ---
    responses:
      200:
        description: A single user item
    Updates the hyper_params or data_offset on indicated model

    :param id: uuid which represents the model

    :return: updated model
    :raise 404: if there isn't any model with that id
    """
    model = Model.find_one({'id': id})
    hyper_parameters = request.get_json().get('hyper_parameters', dict())
    dataset_offset = request.get_json().get('dataset_offset')

    model_updated = model.update(hyper_parameters, dataset_offset)
    return model_updated.to_mongo().to_dict(), 200


@model_blueprint.route('/s0nar/v1/anomalies/model/<id>/train', methods=['POST'])
@require_api_key
def train_model(id):
    """
    Create dataset
    ---
    parameters:
      - in: path
        name: id
        type: int
        required: true
    responses:
      200:
        description: A single user item
    Trains model on the available workers, also, generates anomaly report and persist trained model

    :param id: uuid which represents the dataset

    :return: 200 and 'training' message
    :raise 404: if there isn't any dataset with that id
    """
    model = Model.find_one({'id': id})
    model.status = ModelStatus.TRAINING.value
    if model.type == ModelTypes.ARIMA.value:
        queue = task_name = 'arima'
    elif model.type == ModelTypes.LSTM_CPU.value:
        queue = task_name = 'lstm-cpu'
    elif model.type == ModelTypes.LSTM_GPU.value:
        queue = task_name = 'lstm-gpu'
    celery_app.send_task(task_name, queue=queue, kwargs=dict(model_id=model.id))
    model.save()
    return 'training', 200
