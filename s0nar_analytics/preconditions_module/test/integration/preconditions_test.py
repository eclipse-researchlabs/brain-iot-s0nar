from preconditions_module.src import preconditions_module
import utils


def test_preconditions(dataset):
    """ Test preconditions with original datasets """
    (passed, new_data) = preconditions_module.all_preconditions(dataset)
    assert passed, "data does not pass the test"


def test_preconditions_gaps(dataset):
    """ Test preconditions with low percentage of gaps """
    dataset.data = utils.remove_values(dataset.data, percentage=0.001)
    (passed, new_data) = preconditions_module.all_preconditions(dataset)
    assert passed, "data does not pass the test"


def test_preconditions_too_much_gaps(dataset):
    """ Test preconditions with high percentage of gaps  """
    dataset.data = utils.remove_values(dataset.data, percentage=0.4)
    (passed, new_data) = preconditions_module.all_preconditions(dataset)
    assert not passed, "data does not pass the test"