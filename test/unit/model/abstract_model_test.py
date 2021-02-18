import pytest
from flask_mongoengine import MongoEngine
from mongoengine import disconnect
from src import app



class AbstractModelTest:
    # ------------------------------------------------------
    # Test configuration
    # ------------------------------------------------------
    db = None

    def setup_class(self):
        print('Setting up test module...')

    def setup_method(self):
        disconnect()
        app.config['MONGODB_SETTINGS']['db'] = 'test'
        db = MongoEngine()
        db.init_app(app)
        self.db = db
        print('Setting up tests...')

    @pytest.fixture(autouse=True)
    def mock(self, mocker):
        # Mocking
        mocker.patch("src.data_model.dataset.save_file_in_s3", return_value='s3://s0nar/dataset/sample.csv')
        mocker.patch("os.remove", return_value=None)

    def teardown_method(self):
        conn = self.db.get_connection()
        conn.drop_database('test')
        print('Tearing down tests...')

    def teardown_class(self):
        print('Tearing down test module...')
