import os

from src import celery_app, celery_logger
from src.celery.ml.anomaly import detect_anomalies_from_arima
from src.celery.ml.dataset import load_dataset_from_path
from src.celery.ml.model.auto_arima import train_arima_model_and_get_mae
from src.celery.ml.persist.auto_arima import persist_autoarima
from src.data_model.anomaly_report import AnomalyReport
from src.data_model.model import Model, ModelStatus
from src.data_source.aws import retrieve_file_from_s3, FileType, save_file_in_s3


@celery_app.task(name='arima', queue='arima')
def arima(model_id, persists=True):
    """
    Train auto-arima model to identify anomalies in time series

    :param model_id: entity model identifier
    :param persists: to save de model's results or not

    :return: None
    :raise Exception: when some internal error happens
    """
    celery_logger.info('=============================================')
    celery_logger.info('Retrieve model from database')
    celery_logger.info('=============================================')
    model = Model.find_one({'id': model_id})
    try:
        celery_logger.info('=============================================')
        celery_logger.info('Download and load dataset')
        celery_logger.info('=============================================')
        file_path = retrieve_file_from_s3(model.dataset.s3_uri, model.dataset.name, FileType.DATASET)
        dataset = load_dataset_from_path(file_path, index=model.index_feature, schema=model.index_schema)
        os.remove(file_path)

        celery_logger.info('=============================================')
        celery_logger.info('Sets minimum elements')
        celery_logger.info('=============================================')
        minimum_elements = model.hyper_parameters.get('min_elements')
        minimum_elements = minimum_elements if minimum_elements is not None else dataset.size * 0.1

        celery_logger.info('=============================================')
        celery_logger.info('Train model and obtain metrics')
        celery_logger.info('=============================================')
        predict_model, metrics = train_arima_model_and_get_mae(dataset, model.target_feature, int(minimum_elements))

        celery_logger.info('=============================================')
        celery_logger.info('Persisting model')
        celery_logger.info('=============================================')
        if persists:
            model_path = persist_autoarima(predict_model)
            model.bin_s3_uri = save_file_in_s3(model_path, FileType.ARIMA_BIN, file_name='{}.pkl'.format(str(model.id.hex)))

        celery_logger.info('=============================================')
        celery_logger.info('Updating Model status')
        celery_logger.info('=============================================')
        model.status = ModelStatus.FINISHED.value
        model.save()

        celery_logger.info('=============================================')
        celery_logger.info('Anomaly detection and report creation')
        celery_logger.info('=============================================')
        threshold = model.hyper_parameters.get('threshold', 0.01)
        anomaly_info = detect_anomalies_from_arima(dataset, metrics, threshold, model.target_feature)
        report = AnomalyReport(model=model, anomalies=list(anomaly_info.T.to_dict().values()), params={
            'threshold': threshold
        })
        report.save()
        return None
    except Exception as ex:
        celery_logger.error(ex)
        model.status = ModelStatus.FAILED.value
        model.raised_exception = str(ex)
        model.save()
        raise Exception
