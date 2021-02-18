import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

dataset_to_test = []

def define_data_to_test():
    url = ""
    index = ""
    target = ""
    dataset_to_test.append(url, index, target)


def remove_values(df_origin: pd.DataFrame, percentage: float = 0.005, plot: bool = False)\
        -> pd.DataFrame:
    """

    :param df_origin:
    :param percentage:
    :param plot:
    :return:
    """
    df_data = df_origin.copy()
    remove_n = int(df_data.count()[0] * percentage)
    print("Number of values to remove ", remove_n)
    drop_indices = np.random.choice(df_data.index, remove_n, replace=False)
    df_subset = df_data.drop(drop_indices, axis=0)
    # ax = df_origin.plot(x="UNE")
    # df_subset.plot(x="UNE", ax=ax)
    # plt.show()
    if plot:
        plt.plot(np.arange(0., remove_n, 1), drop_indices, 'ro')
        plt.show()
        plt.plot(df_data.index, df_data.index, 'bs', drop_indices, drop_indices, 'ro')
    return df_subset


def __read_datasets(collection: list) -> list:
    """
    List of path to dir key to dataframe
    :param collection:
    :return:
    """
    datasets = {}
    path = '~/aws/buckets/'
    for key in collection:
        file_path = os.path.join(path + key + '.csv')
        df_data = pd.read_csv(file_path, sep=',', header=0)
        df_data['unix_ts'] = pd.to_datetime(df_data['unix_ts'], unit='s', origin='unix')
        df_data = df_data.set_index(df_data['unix_ts'])
        for var in collection[key]['target']:
            datasets[key] = df_data[var].to_frame()
            datasets[key + "_modified_by_diff"] = df_data[var].diff().to_frame()
    return datasets


def load_test_set():
    """
    Loads a set of datasets
    :return: The set of datasets
    """
    datasets = {}
    datasets['AMPds/Test/Water_WHW'] = {'index': 'unix_ts', 'target': ['counter']}
    datasets['AMPds/Test/NaturalGas_WHG'] = {'index': 'unix_ts', 'target': ['counter']}
    datasets['AMPds/Test/Electricity_WHE'] = {'index': 'unix_ts', 'target': ['V', 'I', 'Q']}
    # datasets['NILM_energy_disggregation'] = ['NO2 Mean', 'NO2 1st Max Value']
    return __read_datasets(datasets)


def load_roman_dataset():
    """
    Loads the Emalcsa dataset build by Roman for the telva uc
    :return: The dataset mentioned
    """
    dateparse = lambda x: pd.datetime.strptime(x, "%Y-%m-%d")
    df_data = pd.read_csv(
        "~/aws/buckets/brain-iot/datasets/internal/EMALCSA_water_dam/1.Version_with_climate/telva_dataset.csv",
        sep=',', header=0, parse_dates=['date'], date_parser=dateparse, index_col=0)
    df_data.columns = df_data.columns.str.strip()
    return df_data

def load_roman_extended_dataset():
    """
    Loads the Emalcsa dataset build by Roman for the telva uc
    :return: The dataset mentioned
    """
    dateparse = lambda x: pd.datetime.strptime(x, "%Y-%m-%d")
    df_data = pd.read_csv(
        "~/aws/buckets/brain-iot/datasets/internal/EMALCSA_water_dam/1.Version_with_climate/telva_dataset.csv",
        sep=',', header=0, parse_dates=['date'], date_parser=dateparse, index_col=0)
    df_data.columns = df_data.columns.str.strip()

    return df_data
