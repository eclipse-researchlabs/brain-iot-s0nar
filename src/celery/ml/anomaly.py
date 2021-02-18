import pandas as pd
import numpy as np


def detect_anomalies_from_arima(dataset, metrics, threshold, target_feature):
    """
    Detect anomalies using auto-arima tuning metrics

    :param dataset: dataset to analyze
    :param metrics: list with auto-arima training metrics
    :param threshold: anomaly detection threshold
    :param target_feature: feature to analyze

    :return: anomalies dataframe
    """
    fill_empty_train = [0] * (len(dataset) - len(metrics))
    fill_empty_train.extend(metrics)
    metrics = fill_empty_train
    norm_metrics = [float(i) / sum(metrics) for i in metrics]
    dataset['metrics'] = norm_metrics
    df_anomalies = dataset[dataset.metrics > threshold]

    anomalies = pd.DataFrame()

    anomalies['date'] = df_anomalies['date']
    anomalies[target_feature] = df_anomalies[target_feature]
    anomalies['distance'] = df_anomalies['metrics']

    return anomalies


def detect_anomalies_from_lstm(model, train, X_train, time_steps, threshold, target_feature):
    """
    Detect anomalies using the LSTM model prediction

    :param model: tf.model
    :param train: train chunk dataset
    :param X_train: test chunk dataset
    :param time_steps: time step chunk
    :param threshold: anomaly detection threshold
    :param target_feature: feature to analyze

    :return: anomaly detection summary (mean loss and anomalies)
    """
    pred = model.predict(X_train)

    score_df = pd.DataFrame(index=train[time_steps:].index)
    score_df['loss'] = np.mean(np.abs(pred - X_train), axis=1)
    score_df['threshold'] = threshold
    score_df['anomaly'] = score_df.loss > score_df.threshold

    anomalies = pd.DataFrame()

    index_anomalies = list(score_df[score_df.anomaly].index)
    df_anomalies = train[train.index.isin(index_anomalies)]

    anomalies['date'] = df_anomalies['date']
    anomalies[target_feature] = df_anomalies[target_feature]
    anomalies['distance'] = score_df[score_df.anomaly]['loss']

    return anomalies
