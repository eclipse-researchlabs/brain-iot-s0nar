import pandas as pd
import numpy as np


def detect_anomalies_from_arima(df: pd.DataFrame, target_index, target_feature,  window: int, std_level=2):
    """
    Script for anomaly detection given a dataframe containing actuals and forecasted values
    """

    # Replace nulls by 0
    df.replace([np.inf, -np.inf], np.NaN, inplace=True)
    df.fillna(0, inplace=True)

    df["actuals_rolling"] = df[target_feature].rolling(window=window).mean()
    df["predicted_rolling"] = df["predicted"].rolling(window=window).mean()

    # Get error rate as difference between actual values and predicted values
    df["error"] = df["actuals_rolling"] - df["predicted_rolling"]

    error_mean = df["error"].mean()
    error_std = df["error"].std()

    upper_lim = error_mean + std_level * error_std
    lower_lim = error_mean - std_level * error_std

    df["upper_lim"] = upper_lim
    df["lower_lim"] = lower_lim

    # Determine anomalies as samples exceeding certain deviation values
    anomaly = (df["error"] >= upper_lim) | (df["error"] <= lower_lim)

    df["anomaly_points"] = anomaly

    df["distance"] = abs(df[target_feature] - df.predicted)

    anomalies = df[df.anomaly_points][[target_index, target_feature, 'distance']]

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
