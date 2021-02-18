import os
import requests
import pytest
from src import app, ConfigFlask
import io


from src import app as flask_app
from test.unit.blueprints.abstract_blueprint_test import AbstractBlueprintTest


class TestIntegration(AbstractBlueprintTest):  # get header by inheritance
    # ------------- -----------------------------------------
    # Test configuration
    # ------------------------------------------------------
    @pytest.fixture
    def app(self):
        return flask_app

    # ------------------------------------------------------
    # Test cases
    # ------------------------------------------------------
    @staticmethod
    def get_arima_data(dataset_response):

        return {
                        "type": "arima",
                        "target_feature": dataset_response["descriptors"]["target_feature"],
                        "index": dataset_response["descriptors"]["index"],
                        "index_schema": dataset_response["descriptors"]["index_schema"],
                        "hyper_parameters": {
                            "min_elements": "50"
                        }
                }

    @staticmethod
    def get_lstm_cpu_data(dataset_response):

        return {
                        "type": "lstm_cpu",
                        "target_feature": dataset_response["descriptors"]["target_feature"],
                        "index": dataset_response["descriptors"]["index"],
                        "index_schema": dataset_response["descriptors"]["index_schema"],
                        "hyper_parameters": {
                        }
                }

    @staticmethod
    def get_lstm_gpu_data(dataset_response):

        return {
                        "type": "lstm_gpu",
                        "target_feature": dataset_response["descriptors"]["target_feature"],
                        "index": dataset_response["descriptors"]["index"],
                        "index_schema": dataset_response["descriptors"]["index_schema"],
                        "hyper_parameters": {
                        }
                }
    def test_save_dataset(self, dataset, client):
        # get number of uploaded datasets
        # response = requests.get("http://localhost:" + str(ConfigFlask.PORT) + '/s0nar/v1/dataset')
        # assert response.status_code == 200, "Get datasets failed"
        # assert len(response.json()) == 0, "Testing BD is not empty"
        # upload dataset

        data = {
            'name': dataset["values"]["name"],
            'target_index': dataset["values"]["target_index"],
            'target_feature': dataset["values"]["target_feature"],
            'target_frequency': dataset["values"]["target_frequency"],
            'index_schema': dataset["values"]["index_schema"],
            'index_frequency': dataset["values"]["index_frequency"],
        }
        data['dataset'] = dataset['files']['dataset']
        response = client.post('/s0nar/v1/dataset',
                               data=data,
                               content_type="multipart/form-data",
                               headers=self.headers)
        assert response.status_code == 200, "Upload dataset failed with dataset " + dataset["values"]["name"]

        # check number of uploaded dataset is bigger than before
        # create ARIMA
        response = response.json
        dataset_id = response["_id"]
        response_arima = client.post("/s0nar/v1/anomalies/" + dataset_id + "/model",
                                 json=self.get_arima_data(response),
                                 headers=self.headers)
        assert response_arima.status_code == 200, "Create model failed with dataset ID " + dataset_id

        # create CPU LSTM
        dataset_id = response["_id"]
        response_lstm = client.post("/s0nar/v1/anomalies/" + dataset_id + "/model",
                                 json=self.get_lstm_cpu_data(response),
                                 headers=self.headers)
        assert response_lstm.status_code == 200, "Create model failed with dataset ID " + dataset_id

        # train model
        #model_id = response.json()["_id"]
        #response = requests.post("http://localhost:" + str(ConfigFlask.PORT) + "/s0nar/v1/anomalies/model/" + model_id + "/train",
        #                         headers=self.headers)
        #assert response.status_code == 200, "Train model failed with model ID " + model_id

        # # get report
        # report_id = response.json()["_id"]
        # response = requests.post("http://localhost:" + str(ConfigFlask.PORT) + "/s0nar/v1/anomaly/" + report_id,
        #                          headers=self.headers)
        # assert response.status_code == 200, "Get report failed with report ID " + report_id
