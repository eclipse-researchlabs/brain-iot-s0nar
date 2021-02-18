from src.data_model.dataset import Dataset
from test.unit.model.abstract_model_test import AbstractModelTest


class TestDatasetModel(AbstractModelTest):
    # ------------------------------------------------------
    # Test cases
    # ------------------------------------------------------
    def test_create_and_find_one_dataset(self):
        ds_id = Dataset(name='example.csv').create('/tmp/example.csv')
        dataset = Dataset.find_one({'id': ds_id})
        assert dataset.id is not None
        assert dataset.s3_uri == 's3://s0nar/dataset/sample.csv'

    def test_find_all_dataset(self):
        Dataset(name='example.csv').create('/tmp/example.csv')
        Dataset(name='example_1.csv').create('/tmp/example_1.csv')
        assert len(Dataset.find_all()) == 2

    def test_find_one_and_replace_dataset(self, mocker):
        mocker.patch("src.data_model.dataset.save_file_in_s3", return_value='s3://s0nar/dataset/sample2.csv')
        ds_id = Dataset(name='example.csv').create('/tmp/example.csv')
        dataset = Dataset.find_one({'id': ds_id})
        new_dataset = dataset.replace('dataset/sample2.csv')
        dataset = Dataset.find_one({'id': new_dataset.id})
        assert dataset.s3_uri == 's3://s0nar/dataset/sample2.csv'
        assert dataset.to_mongo().to_dict().get('previous_version').get('_id').hex == ds_id.hex

    def test_delete_dataset(self):
        assert len(Dataset.find_all()) == 0
        Dataset(name='example.csv').create('/tmp/example.csv')
        Dataset(name='example_1.csv').create('/tmp/example_1.csv')
        assert len(Dataset.find_all()) == 2
        dataset = Dataset.find_all()[0]
        dataset.custom_delete(id=dataset.id)
        assert len(Dataset.find_all()) == 1
