import pandas as pd
from s0nar_analytics.data_models import extended_dataset

THRESHOLD = 0.2


def interpolation(df_data: pd.DataFrame, delta_limit: pd.Timedelta = pd.Timedelta(10, 'd'), std_limit: float = 0.5):
    """
    Evaluates if it is possible to interpolate a data series and interpolates if the conditions are acomplish
    :param df_data: Dataframe
    :param delta_limit:
    :param std_limit: Limit of std value
    :return: Evaluation of the conditions to interpolate
    """
    # gap size
    df_copy = df_data.copy()
    df_copy.reset_index(inplace=True)
    if (df_copy.iloc[:, 0].diff() > delta_limit).any():
        return False, df_data
    # std value
    df_norm = df_data.div(df_data.max(), axis='columns')
    if (df_norm.std() > std_limit).any():
        return False, df_data
    # interpolation
    freq_index = pd.date_range(df_data.index[0], df_data.index[-1], normalize=True, freq=pd.infer_freq(df_data.index))
    df_reindex = df_data.reindex(freq_index)
    df_reindex.interpolate(inplace=True, method='linear') # limit parameter
    return True, df_reindex


def resample(extended_data: extended_dataset.ExtendedDataset, percent_gaps: float = 0.05) -> extended_dataset.ExtendedDataset:
    """
    Evaluates if it is possible to resample a data series
    :param extended_data: Data of the dataframe
    :param percent_gaps: Maximum percentage of gaps alowed
    :return:
    """
    # std freq
    if extended_data.target_freq is not None and extended_data.index_freq > extended_data.target_freq:
        return False, extended_data
    if extended_data.calc_index_freq() > extended_data.index_freq * (1 + THRESHOLD):  # 0.2 threshold
        return False, extended_data
    # gap number
    if not valid_freq(extended_data, error=percent_gaps):
        return False, extended_data
    if extended_data.target_freq is None:
        time = extended_data.calc_index_freq()
        time_unit = 'seconds'
        freq_unit = ['days', 'hours', 'minutes', 'seconds']
        for i in range(0, len(time.components) - 1, 1):
            if time.components[i] != 0:
                time_unit = freq_unit[i]
                break
        freq = time + pd.Timedelta(5, unit=time_unit)
        extended_data.data = extended_data.data.resample(freq).mean()
    else:
        extended_data.data = extended_data.data.resample(extended_data.target_freq).mean()
    return True, extended_data


def valid_size(df_index: pd.DatetimeIndex, seasonality: int, min_size: int = 20) -> bool:
    """
    Validation of the size of the dataframe
    :param df_index: Dataframe index to validate
    :param seasonality: Seasonality of the dataframe
    :param min_size: Minimum size allowed of the number of data points per seasonality frequency
    :return: The success of the validation
    """
    freq_index = pd.date_range(df_index[0], df_index[-1], normalize=True, freq=seasonality)
    if seasonality.components[0] != 0:
        freq_index = freq_index[freq_index.floor('D').isin(df_index)]
    elif seasonality.components[1] != 0:
        freq_index = freq_index[freq_index.floor('H').isin(df_index)]
    elif seasonality.components[2] != 0:
        freq_index = freq_index[freq_index.floor('M').isin(df_index)]
    elif seasonality.components[3] != 0:
        freq_index = freq_index[freq_index.floor('S').isin(df_index)]
    else:
        freq_index = freq_index[freq_index.floor('s').isin(df_index)]
    return freq_index.size > min_size


def valid_freq(extended_data: extended_dataset.ExtendedDataset, error: float = 0.2) -> bool:
    """
    Validation of the frequency of the dataframe
    :param extended_data: Dataframe to validate
    :param error: Maximum permited error
    :return: The success of the validation
    """
    std_limit = extended_data.target_freq * error
    df_data = extended_data.data.copy()
    std = df_data.index.to_series().diff().std()
    return std <= std_limit


def all_preconditions(extended_data: extended_dataset.ExtendedDataset):
    """
    Evaluates all preconditions and modifies the dataframe when necessary
    :param extended_data: Extended dataframe
    :return: the achievement of the preconditions by the dataframe and the dataframe modified if necessary
    """
    if valid_size(extended_data.data.index, seasonality=extended_data.index_freq):
        # Fill small gaps if possible
        interpolated, extended_data.data = interpolation(extended_data.data, delta_limit=extended_data.index_freq * 5)
        if extended_data.operation == 'prediction':
            resampled, new_data = resample(extended_data)
            if resampled:
                extended_data = new_data
                return resampled, extended_data
        if valid_freq(extended_data):
            return True, extended_data
    return False, None
