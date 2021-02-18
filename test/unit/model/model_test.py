import pytest

from datetime import datetime

from mongoengine import ValidationError

from src.data_model.dataset import Dataset
from src.data_model.model import Model, ModelTypes
from test.unit.model.abstract_model_test import AbstractModelTest


class TestModel(AbstractModelTest):
    # ------------------------------------------------------
    # Test cases
    # ------------------------------------------------------
    def test_create_model(self):
        dataset = Dataset(name='example.csv')
        dataset_id = dataset.create('/tmp/example.csv')
        dataset = Dataset.find_one({'id': dataset_id})

        model = Model(dataset=dataset, type=ModelTypes.ARIMA.name, target_feature='water_flow').create()
        assert model is not None

    def test_create_without_dataset_model(self):
        Dataset(name='example.csv').create('/tmp/example.csv')
        with pytest.raises(ValidationError):
            Model(type=ModelTypes.ARIMA.name, target_feature='water_flow').create()

    def test_find_one_and_update_model_and_check_all_models(self):
        dataset = Dataset(name='example.csv')
        dataset_id = dataset.create('/tmp/example.csv')
        dataset = Dataset.find_one({'id': dataset_id})

        model = Model(dataset=dataset, type=ModelTypes.ARIMA.name, target_feature='water_flow').create()

        model = Model.find_one({'id': model.id})
        m = model.update(hyper_parameters={'loss': 'mae', 'time_steps': 30}, dataset_offset=datetime(2012, 2, 2, 6, 35, 6, 764))
        model = Model.find_one({'id': m.id})
        assert model.dataset_offset is not None
        assert model.hyper_parameters.get('time_steps') == 30
        assert len(Model.find_all({'type': ModelTypes.ARIMA.name})) == 2
