from flask import Blueprint, jsonify, request
from src.blueprints.utils.api_key import require_api_key
from src.data_model.prediction_report import PredictionReport

prediction_blueprint = Blueprint("prediction", __name__)


@prediction_blueprint.route('/s0nar/v1/prediction/<model_id>', methods=['GET'])
@require_api_key
def get_prediction_report(model_id):
    """
    Get anomaly report by id
    ---
    parameters:
      - in: path
        name: anomaly_id
        type: int
        required: true
    responses:
      200:
        description: Success

    Retrieves report by its id

    :param anomaly_id: uuid which represents the report

    :return: AnomalyReport
    :raise 404: if there isn't any report with that id
    """
    return PredictionReport.find_one({'id': model_id}).to_mongo().to_dict(), 200


@prediction_blueprint.route('/s0nar/v1/prediction', methods=['GET'])
@require_api_key
def get_all_prediction_reports():
    """
    Get all reports
    ---
    responses:
      200:
        description: Success

    Retrieves all anomalies reports

    :return: list with all persisted reports
    """
    filters = {}

    if request.get_json() is not None:
        if request.get_json().get('model'):
            filters['model'] = request.get_json().get('model')

    response = [report.to_mongo().to_dict() for report in PredictionReport.find_all(filters)]
    return jsonify(response), 200
