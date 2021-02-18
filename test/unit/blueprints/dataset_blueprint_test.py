import os
import pytest
import io
from io import BytesIO
from uuid import UUID

from src import app as flask_app
from src.data_model.dataset import Dataset
from test.unit.blueprints.abstract_blueprint_test import AbstractBlueprintTest


class TestDatasetBlueprint(AbstractBlueprintTest):
    # ------------- -----------------------------------------
    # Test configuration
    # ------------------------------------------------------
    @pytest.fixture
    def app(self, mocker):
        # Mock entities responses
        mock_dataset = Dataset(name='sample.csv', s3_uri='', id=UUID('28892353-5c96-4774-9047-8dca3a3003a0'))
        mock_replaced_dataset = mock_updated_dataset = mock_dataset
        mock_updated_dataset.s3_uri = 's3://s0nar/datasets/sample_updated.csv'
        mock_replaced_dataset.s3_uri = 's3://s0nar/datasets/sample_replaced.csv'

        # Mock functions
        mocker.patch("src.data_model.dataset.Dataset.find_all", return_value=[])
        mocker.patch("src.data_model.dataset.Dataset.create", return_value='dataset_id')
        mocker.patch("src.data_model.dataset.Dataset.find_one", return_value=mock_dataset)
        mocker.patch("src.blueprints.dataset_blueprint.retrieve_file_from_s3", return_value="/tmp/sample.csv")
        return flask_app

    # ------------------------------------------------------
    # Test cases
    # ------------------------------------------------------
    def test_get_all_datasets(self, client):
        response = client.get('/s0nar/v1/dataset')
        assert response.status_code == 200
        assert response.json == []

    """
    def test_save_dataset(self, client, dataset):
        response = client.post('/s0nar/v1/dataset',
                               data={
                                    'name': dataset["values"]["name"],
                                    'dataset': dataset["files"]["dataset"],
                                    'target_index': dataset["values"]["target_index"],
                                    'target_feature': dataset["values"]["target_feature"],
                                    'target_frequency':dataset["values"]["target_frequency"],
                                    'index_schema':dataset["values"]["index_schema"],
                                    'index_frequency':dataset["values"]["index_frequency"],
                                    'files': io.BytesIO(bytes(open("/home/blancabr/aws/buckets/brain-iot/datasets/internal/EMALCSA_water_dam/1.Version_with_climate/telva_dataset.csv").read(),encoding="utf-8"))
                                },
                               content_type="multipart/form-data",
                               headers=self.headers)

        assert response.status_code == 200
    """

    def test_get_dataset_details_by_id(self, client):
        response = client.get('/s0nar/v1/dataset/13/details', headers=self.headers)
        assert response.status_code == 200
        assert response.json.get('_id') == '28892353-5c96-4774-9047-8dca3a3003a0'
