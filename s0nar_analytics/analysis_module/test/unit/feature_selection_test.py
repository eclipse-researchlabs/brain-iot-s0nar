import pytest
from analysis_module.src import analysis_module


# Edge test cases
#
def test_selection_of_covar_(dataset):
    """ Normal case test """
    analysis_module.generate_variables(dataset)
    analysis_module.feature_selection(dataset)