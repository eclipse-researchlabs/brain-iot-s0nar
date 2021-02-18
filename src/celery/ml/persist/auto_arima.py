import time
import joblib

from pathlib import Path


def persist_autoarima(model):
    """
    Saves auto-arima model in a file

    :param model: auto-arima model

    :return: persisted model path
    """
    folder = '/tmp/models/arima/'
    Path(folder).mkdir(parents=True, exist_ok=True)
    pickle_tgt = "{}arima_{}.pkl".format(folder, str(int(time.time())))
    joblib.dump(model, pickle_tgt, compress=3)
    return pickle_tgt


def load_autoarima(model_path):
    """
    Loads auto-arima model from file

    :param model_path: where is the bin file
    :return: auto-arima model
    """
    return joblib.load(model_path)
