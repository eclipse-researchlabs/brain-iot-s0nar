import time

from pathlib import Path
from tensorflow_core.python.keras.saving.model_config import model_from_json


def persist_nn(model):
    """
    Persists neural network

    :param model: LSTM model

    :return: neural network json definition and h5 file with neural network weights
    """
    id = str(int(time.time()))
    folder = '/tmp/models/lstm/'
    Path(folder).mkdir(parents=True, exist_ok=True)
    # Persists model info
    json_file = id + '.json'
    model_json = model.to_json()
    with open(folder+json_file, 'w') as info_file:
        info_file.write(model_json)
    # Persist nn weights
    weights_file = id + '.h5'
    model.save_weights(folder + weights_file)
    return folder+json_file, folder+weights_file


def load_nn(json_path, weights_path):
    """
    Loads LSTM model from its definition files

    :param json_path: model info
    :param weights_path: neural network weights (.h5 file)

    :return: tf LSTM model
    """
    # Load model info
    info_file = open(json_path, 'r')
    model_info = info_file.read()
    info_file.close()
    # Load weights
    model = model_from_json(model_info)
    model.load_weights(weights_path)
    return model
