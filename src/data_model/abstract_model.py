from uuid import uuid4
from datetime import datetime
from src import db


class AbstractModel(object):
    id = db.UUIDField(default=lambda: uuid4(), primary_key=True)
    creation_date = db.DateTimeField(required=True, default=datetime.now)

    @classmethod
    def find_all(cls, filters={}):
        return cls.objects(**filters)

    @classmethod
    def find_one(cls, filters):
        return cls.objects.get(**filters)

    @classmethod
    def custom_delete(cls, id):
        cls.objects.get(id=id).delete()
