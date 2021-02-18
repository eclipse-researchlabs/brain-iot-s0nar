from src import db
from src.data_model.abstract_model import AbstractModel
from src.data_model.model import Model


class PredictionReport(AbstractModel, db.Document):
    model = db.ReferenceField(Model, required=True)
    predictions = db.ListField(required=True)
    params = db.DictField(required=False)
