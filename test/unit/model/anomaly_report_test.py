from src.data_model.anomaly_report import AnomalyReport
from src.data_model.dataset import Dataset
from src.data_model.model import ModelTypes, Model
from test.unit.model.abstract_model_test import AbstractModelTest


class TestDatasetModel(AbstractModelTest):
    # ------------------------------------------------------
    # Test cases
    # ------------------------------------------------------
    def test_create_report(self):
        # Create dataset
        dataset = Dataset(name='example.csv')
        dataset.create('/tmp/example.csv')
        # Create model
        model = Model(dataset=dataset, type=ModelTypes.ARIMA.name, target_feature='water_flow').create()
        # Create report
        AnomalyReport(model=model, anomalies=[1, 3, 5, 7, 9]).save()
        # Retrieve and assert
        model_id = Model.find_all()[0].id
        report = AnomalyReport.find_one({'model': model_id})
        assert report is not None
