from preconditions_module.src import preconditions_module
import utils

"""
Test the different resample methods
"""


def test_resample_method_normal_case(resample_dataset, resample_threshold):
    """ Tests normal case """
    resampled, new_dataset = preconditions_module.resample(resample_dataset)
    assert resampled
    assert new_dataset.calc_index_freq() <= resample_dataset.target_freq * (1 + resample_threshold) and \
           (new_dataset.calc_index_freq() >= resample_dataset.target_freq * (1 - resample_threshold))


def test_resample_method_much_gaps(resample_dataset):
    """ Tests percentage of removed values too high to acomplish the resample condition """
    resample_dataset.data = utils.remove_values(resample_dataset.data, percentage=0.4, plot=False)
    resampled, new_dataset = preconditions_module.resample(resample_dataset)
    assert not resampled
