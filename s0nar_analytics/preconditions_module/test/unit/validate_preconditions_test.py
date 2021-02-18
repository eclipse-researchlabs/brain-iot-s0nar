from preconditions_module.src import preconditions_module
import utils
import pandas as pd


def test_preconditions_validation_size(dataset):
    value = preconditions_module.valid_size(dataset.data.index, pd.infer_freq(dataset.data.index))
    assert value


def test_preconditions_validation_freq(dataset):
    assert preconditions_module.valid_freq(dataset)
    dataset.data = utils.remove_values(dataset.data, percentage=0.2)
    assert not preconditions_module.valid_freq(dataset)


# Test interpolation precondition normal case

# Test interpolation precondition with hugh gaps

# Test interpolation precondition with anomalous period

# Test resample precondition normal case

# Test resample precondition with two different seasonalities

# Test resample precondition with different data points per period

# Test resample preconditions with a lot of small gaps
