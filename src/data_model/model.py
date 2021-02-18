from enum import Enum

from src import db
from src.data_model.abstract_model import AbstractModel
from src.data_model.dataset import Dataset


class ModelTypes(Enum):
    ARIMA = 'ARIMA'
    LSTM_CPU = 'LSTM_CPU'
    LSTM_GPU = 'LSTM_GPU'


class ModelStatus(Enum):
    INACTIVE = 'INACTIVE'
    TRAINING = 'TRAINING'
    FINISHED = 'FINISHED'
    FAILED = 'FAILED'


class Model(AbstractModel, db.Document):
    bin_s3_uri = db.StringField(required=False)
    json_s3_uri = db.StringField(required=False)
    dataset = db.ReferenceField(Dataset, required=True)
    type = db.StringField(required=True)
    status = db.StringField(required=True)
    target_feature = db.StringField(required=True)
    index_feature = db.StringField(required=False)
    index_schema = db.StringField(required=False)
    hyper_parameters = db.DictField(required=False)
    metrics = db.DictField(required=False)
    dataset_offset = db.DateTimeField(required=False)
    raised_exception = db.StringField(required=False)
    previous_model = db.ReferenceField('self', required=False)

    def generate_name(self):
        return '{}-{}-{}'.format(self.dataset.name, self.type, self.creation_date)

    def create(self):
        self.status = ModelStatus.INACTIVE.value
        self.save()
        return self

    def update(self, hyper_parameters, dataset_offset):
        model = Model(dataset=self.dataset,
                      type=self.type,
                      status=ModelStatus.INACTIVE.value,
                      target_feature=self.target_feature,
                      hyper_parameters=hyper_parameters,
                      dataset_offset=dataset_offset,
                      previous_model=self)
        model.save()
        return model