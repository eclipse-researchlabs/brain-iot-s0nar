import os
from flask import Blueprint, request, send_file, jsonify
from time import time

from src import ConfigFlask
from src.blueprints.utils.api_key import require_api_key
from src.data_model.dataset_descriptor import DatasetDescriptor
from src.data_model.dataset import Dataset
from src.data_source.aws import retrieve_file_from_s3, FileType
from s0nar_analytics.preconditions_module.src import preconditions_module
from s0nar_analytics.analysis_module.src import analysis_module
from s0nar_analytics.data_models import extended_dataset

dataset_blueprint = Blueprint("dataset", __name__)


def _save_attached_dataset(name, file):
    """
    Creates an entity which represents a dataset saved on Amazon's S3 bucket

    :param name: file name which will have in Amazon's S3 bucket
    :param file: attached file binary content

    :return: local path where attached file has been saved
    """
    path = os.path.join(ConfigFlask.UPLOAD_FOLDER, name)
    file.save(path)

    return path


@dataset_blueprint.route('/s0nar/v1/dataset', methods=['POST'])
def create_dataset():
    """
    Create dataset
    ---
    responses:
      200:
        description: A single user item
    Creates an entity which represents a dataset saved on Amazon's S3 bucket

    :return: dataset entity persisted on database
    """
    file = request.files['dataset']
    name = request.form.get('name{}'.format(os.path.splitext(file.filename)), file.filename)

    descriptors = dict(request.form)
    if 'name' in descriptors:
        del descriptors['name']

    path = _save_attached_dataset(name, file)

    index = request.form.get('target_index')
    target = request.form.get('target_feature')
    frequency = request.form.get('target_frequency')
    schema = request.form.get('index_schema')
    index_freq = request.form.get('index_frequency')

    # Preconditions evaluation
    edata = extended_dataset.ExtendedDataset(path, index, target, frequency, index_freq=index_freq, index_schema=schema)
    (passed, dataset) = preconditions_module.all_preconditions(edata)
    if not passed:
        return 'Unprocessable Entity', 422

    # Feature generation
    dataset = analysis_module.generate_variables(dataset)
    # Feature selection
    dataset = analysis_module.feature_selection(dataset)

    descriptors = DatasetDescriptor(
      index=dataset.index,
      target_feature=dataset.target_feature,
      target_frequency=frequency,
      index_schema=dataset.index_schema,
      index_frequency=index_freq
    )
    dataset = Dataset(name=name, descriptors=descriptors)
    # dataset.set_descriptors(descriptors)
    dataset.create(path)

    return dataset.to_mongo().to_dict(), 200


@dataset_blueprint.route('/s0nar/v1/dataset/<id>/details', methods=['GET'])
def retrieve_dataset(id):
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
    Retrieves dataset by its id

    :param id: uuid which represents the dataset

    :return: Dataset
    :raise 404: if there isn't any dataset with that id
    """
    dataset = Dataset.find_one({'id': id}).to_mongo().to_dict()
    return dataset, 200


@dataset_blueprint.route('/s0nar/v1/dataset/<id>', methods=['GET'])
@require_api_key
def download_dataset(id):
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
    Downloads dataset by its id

    :param id: uuid which represents the dataset

    :return: binary content of dataset file, in other words, the dataset content
    :raise 404: if there isn't any dataset with that id
    """
    dataset = Dataset.find_one({'id': id})
    retrieved_file = retrieve_file_from_s3(dataset.s3_uri, dataset.name, FileType.DATASET)
    return send_file(retrieved_file, attachment_filename=dataset.name)


@dataset_blueprint.route('/s0nar/v1/dataset', methods=['GET'])
def retrieve_all_datasets():
    """
    Retrieve dataset
    ---
    responses:
      200:
        description: A single user item
    Retrieves all datasets

    :return: list with all persisted datasets
    """
    response = [dataset.to_mongo().to_dict() for dataset in Dataset.find_all()]
    return jsonify(response), 200


@dataset_blueprint.route('/s0nar/v1/dataset/<id>', methods=['PATCH'])
# @api.doc(params={'id': "Id of the dataset"},
#          responses={200: 'Ok'})
@require_api_key
def update_dataset(id):
    """
    Update dataset by id
    ---
    parameters:
      - in: path
        name: id
        type: int
        required: true
    responses:
      200:
        description: A single user item

    Increase the dataset content, in other words, add more rows at the end of dataset

    :param id: uuid which represents the dataset

    :return: updated dataset
    :raise 404: if there isn't any dataset with that id
    """
    file = request.files['dataset']

    dataset = Dataset.find_one({'id': id})
    files = [retrieve_file_from_s3(dataset.s3_uri, dataset.name + '.' + str(int(time())), FileType.DATASET),
             _save_attached_dataset(dataset.name + '.' + str(int(time())), file)]

    # Concatenate all version
    combined_file = "/tmp/{}".format(dataset.name)
    with open(combined_file, "wb") as outfile:
        for f in files:
            with open(f, "rb") as infile:
                outfile.write(infile.read())

    # Clean local files
    for f in files:
        os.remove(f)

    # Update new dataset
    dataset.update(combined_file)
    return dataset.to_mongo().to_dict(), 200


@dataset_blueprint.route('/s0nar/v1/dataset/<id>', methods=['PUT'])
@require_api_key
def replace_dataset(id):
    """
    Replace dataset by an id
    ---
    parameters:
      - in: path
        name: id
        type: int
        required: true
    responses:
      200:
        description: A single user item
    Replace the dataset file and inherit their attributes, also add old dataset reference as an attribute

    :param id: uuid which represents the dataset

    :return: replaced dataset
    :raise 404: if there isn't any dataset with that id
    """
    file = request.files['dataset']

    dataset = Dataset.find_one({'id': id})
    path = _save_attached_dataset(dataset.name, file)

    updated_dataset = dataset.replace(path)
    return updated_dataset.to_mongo().to_dict(), 200
