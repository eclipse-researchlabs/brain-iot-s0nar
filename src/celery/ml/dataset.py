import pandas as pd


def load_dataset_from_path(dataset_path, index="", schema=None):
    """
    Load dataset from local path

    :param dataset_path: where is the file
    :param index: data offset to filter the dataframe
    :param schema: schema for the index parser
    :return: dataframe to analyze
    """

    if schema:
        date_parse = lambda x: pd.to_datetime(x, format=schema)
    else:
        date_parse = lambda x: x

    if index == "":
        df = pd.read_csv(dataset_path, index_col=0, header=0)
    elif schema == "":
        df = pd.read_csv(dataset_path, index=index, date_parser=date_parse, header=0)
    else:
        df = pd.read_csv(dataset_path, parse_dates=[index], date_parser=date_parse, header=0)
    return df
