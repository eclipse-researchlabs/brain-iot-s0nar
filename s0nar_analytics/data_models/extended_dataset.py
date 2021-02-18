from enum import Enum
import pandas as pd
import matplotlib.pyplot as plt
import datetime


class OperationType(Enum):
    PREDICTION = 1
    ANOMALY = 2
    BOTH = 3


class ExtendedDataset(object):

    def __init__(self, path, index, feature, target_freq, index_freq=None, index_schema=None, field_separator=',',
                 operation=OperationType.BOTH):
        dateparse = None
        if index_schema:
            dateparse = lambda x: pd.datetime.strptime(x, index_schema)
        df_data = pd.read_csv(path, sep=field_separator, header=0, parse_dates=[index], date_parser=dateparse, index_col=0)
        df_data.columns = df_data.columns.str.strip()
        self.data = df_data
        self.operation = operation
        self.index = index
        if index_freq is not None:
            self.index_freq = pd.Timedelta(index_freq)
        else:
            self.index_freq = self.calc_index_freq()
        self.index_schema = index_schema
        self.field_separator = field_separator
        self.target_feature = str(feature)
        self.target_freq = pd.Timedelta(target_freq)
        if self.index_freq is None:
            self.index_freq = self.calc_index_freq()

    def get_covariables(self) -> list:
        """
        Get the list of co-variables of a extended dataset
        :return:
        """
        target_columns = list(self.data.columns.values)
        return list(set(target_columns) - set([self.target_feature]))

    def calc_index_freq(self):
        return self.data.index.to_series().diff().mean()

    def read_data(self, path):
        dateparse = lambda x: pd.datetime.strptime(x, self.index_schema)
        df_data = pd.read_csv(path, sep=self.field_separator, header=0, parse_dates=[self.index], date_parser=dateparse,
                              index_col=0)
        df_data.columns = df_data.columns.str.strip()
        self.data = df_data

    def freq_to_str(self):
        resolution = self.index_freq.resolution_string
        freq = str(self.index_freq.days) + resolution if resolution == 'D' else str(self.index_freq.seconds) + 'S'
        return freq

    def write_data(self, path):
        self.data.to_csv(path, index=self.index)

    def plot(self):
        self.data.plot()
        plt.show()
