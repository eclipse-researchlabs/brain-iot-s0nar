from flask import Blueprint, jsonify, request
from src.blueprints.utils.api_key import require_api_key
from src.data_model.anomaly_report import AnomalyReport

anomaly_blueprint = Blueprint("anomaly", __name__)


@anomaly_blueprint.route('/s0nar/v1/anomaly/<anomaly_id>', methods=['GET'])
@require_api_key
def get_anomaly_report(anomaly_id):
    """
    Get anomaly report by id
    ---
    parameters:
      - in: path
        name: anomaly_id
        type: string
        required: true
    responses:
      200:
        description: Success

    Retrieves report by its id

    :param anomaly_id: uuid which represents the report

    :return: AnomalyReport
    :raise 404: if there isn't any report with that id
    """
    return AnomalyReport.find_one({'id': anomaly_id}).to_mongo().to_dict(), 200


@anomaly_blueprint.route('/s0nar/v1/anomaly', methods=['GET'])
@require_api_key
def get_all_reports():
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

    response = [report.to_mongo().to_dict() for report in AnomalyReport.find_all(filters)]
    return jsonify(response), 200


@anomaly_blueprint.route('/s0nar/v1/model/<model_id>/anomaly', methods=['GET'])
@require_api_key
def get_all_reports_by_model(model_id):
    """
    Get all reports filtered by model
    ---
    parameters:
      - in: path
        name: model_id
        type: string
        required: true
    responses:
      200:
        description: Success

    Retrieves all anomalies reports for the given model

    :return: list with all persisted reports
    """
    response = [report.to_mongo().to_dict() for report in AnomalyReport.find_all({
      'model': model_id
    })]

    return jsonify(response), 200


'''
# TODO:
@anomaly_blueprint.route('/s0nar/v1/anomaly/<anomaly_id>', method=['PATCH'])
@require_api_key
def modify_report_threshold(anomaly_id):
    new_threshold = request.get_json().get('threshold')
    report = AnomalyReport.find_one({'id': anomaly_id})
    report.update(new_threshold)
    [...]
    return report, 200
'''