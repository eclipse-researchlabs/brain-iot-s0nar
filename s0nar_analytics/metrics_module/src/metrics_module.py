import matplotlib.pyplot as plt
import pandas as pd


def get_metrics(df_origin: pd.DataFrame, df_generated: pd.DataFrame, metric: str = 'mse', plot: bool = False) -> list:
    """

    :param df_origin:
    :param df_generated:
    :param metric:
    :param plot:
    :return:
    """
    if plot:
        ((df_origin - df_generated).abs()).plot()
        plt.show()
    df_generated = df_generated.div(df_origin.max(), axis='columns')
    df_origin = df_origin.div(df_origin.max(), axis='columns')
    switcher = {
        'mse': (df_origin - df_generated).abs().sum()/df_origin.count(),
    }
    return switcher.get(metric, "Invalid metric")
