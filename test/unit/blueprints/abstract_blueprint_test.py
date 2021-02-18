from pymongo import MongoClient
from src import ConfigFlask
from src.config import ConfigMongoDB

class AbstractBlueprintTest:
    headers = {'x-api-key': ConfigFlask.API_KEY}
    client = None

    def setup_method(self):
        url = 'mongodb://' + ConfigMongoDB.MONGODB_USERNAME + ':' + ConfigMongoDB.MONGODB_PASSWORD + '@'+ ConfigMongoDB.MONGODB_HOST + ':' + \
              str(ConfigMongoDB.MONGODB_PORT) + '/?authSource=' + ConfigMongoDB.MONGODB_AUTH_SOURCE+'&readPreference=primary&ssl=false'
        self.client = MongoClient(url)

    def teardown_method(self):
        self.client.drop_database(ConfigMongoDB.MONGODB_DB)
        print('Tearing down tests...')