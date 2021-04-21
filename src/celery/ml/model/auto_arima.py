import pmdarima as pm
import numpy as np
import pandas as pd

from tqdm import tqdm
import itertools

from src import app
from sklearn.metrics import mean_absolute_error


def forecasting_arima(dataset: pd.DataFrame, target_index, target_feature, step: int = 10):
    """
    Perform ARIMA forecasting.

    :param dataset: The time series dataset to use for forecasting.
    :param target_index (str): The column to use as index.
    :param target_feature (str): The column to select.
    :param step: The step size to use for forecasting.

    :returns: Predictions, ground truth and dates list.
    """
    predictions = []
    ground_truth = []
    dates = []

    split = int(0.90 * len(dataset))

    if len(dataset) - split < step:
        split = len(dataset) - step

    if split < 0:
        raise Exception(f"Data Set not long enough ({len(dataset)} entries)")

    split = split + (len(dataset) - split) % step

    history = list(np.log10(dataset[target_feature] - dataset[target_feature].min() + 1))

    model = pm.auto_arima(
        history,
        trace=True,
        n_fits=30,
        error_action="ignore",
        suppress_warnings=True,
        seasonal=True,
        stepwise=False,
        random=True,
        n_jobs=12,
    )

    # Use test set for rolling predictions
    # start at split (train max date)
    # end at X_test size
    # Define step size
    for index in tqdm(range(split, len(dataset), step)):

        # Data's length is increasing over time as we get more data points over time
        # Training dataset starts from 0 to index value, which is the test set start + step increment
        data = dataset[:index]

        # Target starts on index value and is incremented by step value
        target = dataset[index : index + step]

        # Train model
        model.fit(np.log10(data[target_feature] - data[target_feature].min() + 1))

        # Predict for the next "step" values - we need to get the length of the target
        # as step value might not be equal in all iterations
        real_step = len(target)
        prediction = 10 ** (model.predict(real_step)) - 1 + data[target_feature].min()

        # Save test set predictions, which is being incrementally done in this rolling window approach
        predictions.append(prediction)
        ground_truth.append(target[target_feature].values)
        dates.append(target[target_index].astype(str))

    predictions = list(itertools.chain(*predictions))
    ground_truth = list(itertools.chain(*ground_truth))
    dates = list(itertools.chain(*dates))

    df_timeseries = pd.DataFrame(
        {target_index: dates, target_feature: ground_truth, "predicted": predictions}
    )

    return model, df_timeseries

