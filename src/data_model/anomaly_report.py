from src import db
from src.data_model.abstract_model import AbstractModel
from src.data_model.model import Model


class AnomalyReport(AbstractModel, db.Document):
    model = db.ReferenceField(Model, required=True)
    anomalies = db.ListField(required=False)
    params = db.DictField(required=False)
