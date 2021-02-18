import os

from src import celery_app, celery_logger
from src.celery.ml.anomaly import detect_anomalies_from_lstm
from src.celery.ml.dataset import load_dataset_from_path
from src.celery.ml.model.lstm_autoencoders import TfContext, train_lstm_autoencoders_model
from src.celery.ml.persist.lstm import persist_nn
from src.data_model.anomaly_report import AnomalyReport
from src.data_model.model import Model, ModelStatus
from src.data_source.aws import retrieve_file_from_s3, FileType, save_file_in_s3


@celery_app.task(name='lstm-cpu', queue='lstm-cpu')
def lstm_cpu(model_id, persists=True):
    """
    Calls __lstm task on CPU context
    """
    return __lstm(model_id, persists, context=TfContext.CPU)


@celery_app.task(name='lstm-gpu', queue='lstm-gpu')
def lstm_gpu(model_id, persists=True):
    """
    Calls __lstm task on GPU context
    """
    return __lstm(model_id, persists, context=TfContext.GPU)


def __lstm(model_id, persists, context):
    """
    Train LSTM network to identify anomalies in time series

    :param model_id: entity model identifier
    :param persists: model's result persists or not
    :param context: TensorFlow execution context

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
        celery_logger.info('Sets hyper params')
        celery_logger.info('=============================================')
        time_steps = model.hyper_parameters.get('time_steps') if model.hyper_parameters.get('time_steps') else 30
        test_size = model.hyper_parameters.get('test_size') if model.hyper_parameters.get('test_size') else 0.01
        optimizer = model.hyper_parameters.get('optimizer') if model.hyper_parameters.get('optimizer') else 'adam'
        loss = model.hyper_parameters.get('loss') if model.hyper_parameters.get('loss') else 'mae'
        threshold = model.hyper_parameters.get('threshold') if model.hyper_parameters.get('threshold') else 0.9

        celery_logger.info('=============================================')
        celery_logger.info('Train model and obtain metrics')
        celery_logger.info('=============================================')
        predict_model, train, X_train = train_lstm_autoencoders_model(dataset, model.target_feature,
                                                                               time_steps, test_size, optimizer,
                                                                               loss, context)
        celery_logger.info('=============================================')
        celery_logger.info('Persisting model')
        celery_logger.info('=============================================')
        if persists:
            info_path, weights_path = persist_nn(predict_model)
            model.bin_s3_uri = save_file_in_s3(info_path, FileType.TENSORFLOW_JSON, file_name='{}.json'.format(str(model.id.hex)))
            model.json_s3_uri = save_file_in_s3(weights_path, FileType.TENSORFLOW_BIN, file_name='{}.h5'.format(str(model.id.hex)))

        celery_logger.info('=============================================')
        celery_logger.info('Updating Model status')
        celery_logger.info('=============================================')
        model.status = ModelStatus.FINISHED.value
        model.save()

        celery_logger.info('=============================================')
        celery_logger.info('Anomaly detection and report creation')
        celery_logger.info('=============================================')
        # Detection
        anomaly_info = detect_anomalies_from_lstm(predict_model, train, X_train, time_steps, threshold, model.target_feature)
        # Report creation
        AnomalyReport(model=model, anomalies=list(anomaly_info.T.to_dict().values()), params={
            'threshold': threshold,
            'time_steps': time_steps
        }).save()

        return None
    except Exception as ex:
        celery_logger.error(ex)
        model.status = ModelStatus.FAILED.value
        model.raised_exception = str(ex)
        model.save()
        raise Exception
