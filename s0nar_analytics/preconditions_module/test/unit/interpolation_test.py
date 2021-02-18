from pandas import Timedelta
from preconditions_module.src import preconditions_module
from metrics_module.src import metrics_module
import utils

"""
Test the different interpolation methods
"""


# def test_interpolation_method_normal_case():
#     """ Tests sample_method() for two integers """
#     test_set = utils.load_roman_dataset()
#     df_generated = utils.remove_values(test_set, percentage=0.01)
#     df_interpolated = preconditions_module.interpolation(df_generated)
#     mse = metrics_module.get_metrics(test_set, df_interpolated)
#     print(mse)
#     assert (mse < 0.001).all()
#
#
# def test_interpolation_method_too_much_gaps():
#     """ Tests sample_method() for two integers """
#     test_set = utils.load_roman_dataset()
#     df_generated = utils.remove_values(test_set, percentage=0.25)
#     df_interpolated = preconditions_module.interpolation(df_generated)
#     mse = metrics_module.get_metrics(test_set, df_interpolated)
#     print(mse)
#     assert not (mse < 0.001).all()
#
#
# def test_interpolation_method_low_interpolation_size():
#     """ Tests sample_method() for two integers """
#     test_set = utils.load_roman_dataset()
#     df_generated = utils.remove_values(test_set, percentage=0.05)
#     df_interpolated = preconditions_module.interpolation(df_generated)
#     mse = metrics_module.get_metrics(test_set, df_interpolated)
#     print(mse)
#     assert not (mse < 0.001).all()
#
#
# def test_interpolation_precondition_normal_case():
#     """ Tests sample_method() for two integers """
#     test_set = utils.load_roman_dataset()
#     df_generated = utils.remove_values(test_set)
#     assert preconditions_module.interpolation_precondition(df_generated)
#
#
# def test_interpolation_precondition_too_much_gaps():
#     """ Tests sample_method() for two integers """
#     test_set = utils.load_roman_dataset()
#     df_generated = utils.remove_values(test_set, percentage=0.5)
#     assert not preconditions_module.interpolation_precondition(df_generated)
#
#
# def test_interpolation_precondition_std_threshold():
#     """ Tests sample_method() for two integers """
#     test_set = utils.load_roman_dataset()
#     df_generated = utils.remove_values(test_set)
#     assert not preconditions_module.interpolation_precondition(df_generated, std_limit=0.1)
#     assert preconditions_module.interpolation_precondition(df_generated, std_limit=0.6)
#
#
# def test_interpolation_precondition_gaps_threshold():
#     """ Tests sample_method() for two integers """
#     test_set = utils.load_roman_dataset()
#     df_generated = utils.remove_values(test_set)
#     assert not preconditions_module.interpolation_precondition(df_generated, delta_limit=Timedelta(1, 'd'))
#     assert preconditions_module.interpolation_precondition(df_generated, delta_limit=Timedelta(10, 'd'))
