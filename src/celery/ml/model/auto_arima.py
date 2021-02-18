import pmdarima as pm

from src import app
from sklearn.metrics import mean_absolute_error


def train_arima_model_and_get_mae(dataset, target_feature, minimum_elements):
    """
    Trains and analyze dataset's time series

    :param dataset: dataFrame to analyze
    :param target_feature: feature to analyze
    :param minimum_elements: how many elements before to start to analyze time series

    :returns Arima model and it's metrics
    """
    metrics = [0] * minimum_elements

    step = 30
    split = int(0.90 * len(dataset))
    split = split + (len(dataset) - split) % step   # adjust the size to fit perfect chunks during test
    model = pm.auto_arima(dataset[:split][target_feature], error_action='ignore', trace=True, suppress_warnings=True)

    for index in range(split, len(dataset), step):
        app.logger.info('Arima model training for element:\t{}'.format(index))
        data = dataset[:index]
        target = dataset[index:index+step]

        # Train model
        model.fit(data[target_feature])

        # Predict
        prediction = model.predict(step)

        # Compute metric
        metrics.append(mean_absolute_error(target[target_feature], prediction))

    return model, metrics

