from enum import Enum

import numpy as np
import tensorflow as tf

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, RepeatVector, TimeDistributed, Input

from tensorflow_core.python.keras import regularizers


class TfContext(Enum):
    CPU = 'CPU',
    GPU = 'GPU'


def train_lstm_autoencoders_model(dataset, target_feature, time_steps=30, test_size=0.01,
                                  optimizer='adam', loss='mae', context=TfContext.CPU):
    """
    Train the LSTM network for analyze the anomalies

    :param dataset: pandas Dataframe to analyze
    :param target_feature: the feature to predict/analyze
    :param time_steps: how many steps
    :param test_size: test size to validate the model
    :param optimizer: which optimazer will be used in training fit stage
    :param loss: loss function that will be used by tensorflow
    :param context: which hardware will be used by tensowflow (CPU or GPU)

    :return: tensorflow model, train dataset to analyze in the anomaly module and X_train (feature to predict
    in narray type)
    """
    # ------------------------------------------------------------------------------
    def __create_dataset(x, y, _time_steps=1):
        """
        Prepare the feature to train the model and also to do future analysis
        """
        xs, ys = [], []
        for i in range(len(x) - _time_steps):
            v = x.iloc[i:(i + _time_steps)].values
            xs.append(v)
            ys.append(y.iloc[i + _time_steps])
        return np.array(xs), np.array(ys)

    # ------------------------------------------------------------------------------
    def __get_rnn_by_context(_context):
        """
        Creates the tf model depending on the execution context

        :param _context: CPU or GPU context

        :return: Tensorflow Secuential model
        """
        if _context == TfContext.CPU:
            from tensorflow.keras.layers import LSTM

            model = Sequential()
            inputs = Input(X_train.shape[1], X_train.shape[2])
            model.add(LSTM(16, return_sequences=True, kernel_regularizer=regularizers.l2(0.00)))
            model.add(LSTM(4, return_sequences=False))
            model.add(RepeatVector(X_train.shape[1]))
            model.add(LSTM(4, return_sequences=True))
            model.add(LSTM(16, return_sequences=True))
            model.add(TimeDistributed(Dense(X_train.shape[2])))

            return model

        elif _context == TfContext.GPU:
            from tensorflow.compat.v1.keras.layers import CuDNNLSTM

            physical_devices = tf.config.list_physical_devices('GPU')
            tf.config.experimental.set_memory_growth(physical_devices[0], True)

            model = Sequential()
            inputs = Input(X_train.shape[1], X_train.shape[2])
            model.add(CuDNNLSTM(16, return_sequences=True, kernel_regularizer=regularizers.l2(0.00)))
            model.add(CuDNNLSTM(4, return_sequences=False))
            model.add(RepeatVector(X_train.shape[1]))
            model.add(CuDNNLSTM(4, return_sequences=True))
            model.add(CuDNNLSTM(16, return_sequences=True))
            model.add(TimeDistributed(Dense(X_train.shape[2])))

            return model
    # ------------------------------------------------------------------------------

    np.random.seed(7)

    # Split dataset
    train, test = train_test_split(dataset, test_size=test_size)

    # Scale datasets
    scaler = StandardScaler()
    scaler = scaler.fit(train[[target_feature]])

    train[target_feature] = scaler.transform(train[[target_feature]])
    test[target_feature] = scaler.transform(test[[target_feature]])

    # Create sequences with time_steps days worth of historical data
    X_train, y_train = __create_dataset(train[[target_feature]], train[target_feature], time_steps)
    # X_test, y_test = __create_dataset(test[[target_feature]], test[target_feature], time_steps)

    # Create LSTM model
    model = __get_rnn_by_context(context)

    model.compile(loss=loss, optimizer=optimizer)

    # Fit model
    model.fit(X_train, y_train, epochs=30, batch_size=10, validation_split=0.05, shuffle=False)

    return model, train, X_train
