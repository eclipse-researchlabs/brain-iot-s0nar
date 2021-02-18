import pytest
import utils
from analysis_module.src import analysis_module


# def test_generation_of_covar_():
#     """ Tests sample_method() for two integers """
#     df_data = utils.load_roman_dataset()
#     df_copy = df_data.copy()
#     columns = list(df_copy.columns.values)
#     columns.remove("water_flow")
#     df_new = analysis_module.generate_variables(df_copy, columns)
#     assert len(df_data.columns) < len(df_new.columns)
#
#
# def test_generation_of_covar_less_time_delta():
#     """ Tests sample_method() for two integers """
#     df_data = utils.load_roman_dataset()
#     df_copy = df_data.copy()
#     time_delta = utils.get_time_delta(df_copy.index)
#     target_time_delta = time_delta * 5
#     columns = list(df_copy.columns.values)
#     columns.remove("water_flow")
#     df_new = analysis_module.generate_variables(df_copy, columns, target_time_delta)
#     # assert time_delta < utils.get_time_delta(df_new.index)
#     # assert target_time_delta == utils.get_time_delta(df_new.index)
#     assert len(df_data.columns) < len(df_new.columns)
#
#
# def test_generation_of_covar_equal_time_delta():
#     """ Tests sample_method() for two integers """
#     df_data = utils.load_roman_dataset()
#     df_copy = df_data.copy()
#     time_delta = utils.get_time_delta(df_copy.index)
#     columns = list(df_copy.columns.values)
#     columns.remove("water_flow")
#     df_new = analysis_module.generate_variables(df_copy, columns, time_delta)
#     assert time_delta == utils.get_time_delta(df_new.index)
#     assert len(df_data.columns) < len(df_new.columns)
#
#
# def test_generation_of_covar_exception_none_vars():
#     """ Tests sample_method() for two integers """
#     with pytest.raises(Exception):
#         analysis_module.generate_variables(None, None)
#
#
# def test_generation_of_covar_exception_case_no_cov():
#     """ Tests sample_method() for two integers """
#     df_data = utils.load_roman_dataset()
#     with pytest.raises(Exception):
#         analysis_module.generate_variables(df_data, None)
#
#
# def test_generation_of_covar_exception_invented_cov():
#     """ Tests sample_method() for two integers """
#     df_data = utils.load_roman_dataset()
#     with pytest.raises(Exception):
#         analysis_module.generate_variables(df_data, ["var that don't exist", "var that don't exist either"])
#
#
# def test_generation_of_covar_exception_no_target_var():
#     """ Tests sample_method() for two integers """
#     df_data = utils.load_roman_dataset()
#     with pytest.raises(Exception):
#         analysis_module.generate_variables(df_data, [])
