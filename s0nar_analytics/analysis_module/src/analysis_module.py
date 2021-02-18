import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from numpy import fill_diagonal
from s0nar_analytics.data_models import extended_dataset


def generate_variables(extended_data: extended_dataset.ExtendedDataset) -> extended_dataset.ExtendedDataset:
    """
    Add variables to the original data with basic arithmetic transformations that can be useful for searching the
    most relevant co-variables set
    :param extended_data: Original data
    :param target_freq: Frequency required for prediction or detection of anomalies. It is also the maximum frequency
    allowed
    :return: Data with the new co-variables added
    """

    covariables_list = extended_data.get_covariables()
    # Check preconditions
    if extended_data.data is None:
        raise AttributeError('Empty dataset')
    # TODO What happens with dataset without covariables ?
    columns = list(extended_data.data.columns.values)
    if len(covariables_list) >= len(columns) or not set(covariables_list).issubset(columns):
        raise AttributeError('Bad co-variable list given')

    if extended_data.index_freq is None:
        current_time_delta = extended_dataset.calc_index_freq()
    else:
        current_time_delta = extended_data.index_freq
    # Check if it is possible to resample the data
    resample_option = extended_data.target_freq is not None and current_time_delta < extended_data.target_freq
    # Create new variables from each co-variable
    for column in covariables_list:
        extended_data.data[column + "_diff"] = extended_data.data[column].diff()
        if resample_option:
            extended_data.data[column + "_std"] = extended_data.data[column].resample(extended_data.target_freq).std()
            extended_data.data[column + "_sum"] = extended_data.data[column].resample(extended_data.target_freq).sum()
            extended_data.data[column + "_median"] = extended_data.data[column].resample(extended_data.target_freq).median()
            extended_data.data[column + "_mean"] = extended_data.data[column].resample(extended_data.target_freq).mean()
    return extended_data


def feature_selection(extended_data: extended_dataset.ExtendedDataset, plot_option: bool = False,
                      correlation_threshold: float = 0.1) -> extended_dataset.ExtendedDataset:
    """
    Performs feature selection to predict or detect anomalies over the target variables, based on the
    correlation between them.
    :param extended_data: Original data
    :param plot_option: Decision of plot the correlation matrix between all the variables, included the generated ones
    :param correlation_threshold: All the co-variables that accomplish the rules between them and have a correlation
     up to  this threshold are included in the best candidate.
    :return: Data with the co-variables chosen as best candidates
    """
    if extended_data.data is None or extended_data.target_feature is None:
        raise AttributeError('Variable given with None value')

    corr = abs(extended_data.data.corr())
    if plot_option:
        sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns)
        plt.show()
    fill_diagonal(corr.values, 0)
    correlation_matrix = corr.copy()
    corr.drop(corr.columns.difference([extended_data.target_feature]), axis=1, inplace=True)
    # Selection of highly correlated features
    corr = abs(corr[extended_data.target_feature])
    # Get correlated vars by target
    relevant_features = corr[corr > correlation_threshold].dropna()
    # Sort features by correlation with the target variables
    relevant_features.sort_values(ascending=False, inplace=True)
    df_solution = pd.DataFrame()
    if len(relevant_features) > 0:
        # Get dependency between the relevant vars selected
        dependent_features = correlation_matrix.loc[relevant_features.index, relevant_features.index]
        conflicts_matrix = dependent_features > correlation_threshold
        index = 0
        iterable = relevant_features.index
        # Remove the linear dependent co-variables by less correlated with the target
        while index < len(iterable):
            conflicts = conflicts_matrix.index[conflicts_matrix[iterable[index]]].to_list()
            iterable = iterable.drop(conflicts)
            conflicts_matrix.drop(conflicts, axis=0, inplace=True)
            index += 1
        df_solution = extended_data.data[iterable]  # Add co-variables
    df_solution.loc[extended_data.target_feature] = extended_data.data[extended_data.target_feature] # Add target variables
    extended_data.data = df_solution
    return extended_data
