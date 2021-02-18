import os

from src import db
from src.data_model.abstract_model import AbstractModel
from src.data_model.dataset_descriptor import DatasetDescriptor
from src.data_source.aws import FileType, save_file_in_s3


class Dataset(AbstractModel, db.Document):
    name = db.StringField(required=True)
    s3_uri = db.StringField(required=True)
    descriptors = db.EmbeddedDocumentField(DatasetDescriptor, required=False)
    previous_version = db.ReferenceField('self', required=False)

    def create(self, path):
        self.s3_uri = save_file_in_s3(path, FileType.DATASET)
        self.save()
        return self.id

    def update(self, new_data_path):
        new_s3_uri = save_file_in_s3(new_data_path, FileType.DATASET, file_name=self.name)
        self.s3_uri = new_s3_uri
        return self

    def replace(self, new_data_path):
        dataset = Dataset(name=self.name, previous_version=self.to_mongo())
        # Upload new chuck to s3
        file_name = '{}_{}'.format(dataset.id.hex, dataset.name)
        new_s3_uri = save_file_in_s3(new_data_path, FileType.DATASET, file_name=file_name)
        os.remove(new_data_path)
        dataset.s3_uri = new_s3_uri

        dataset.save()
        return dataset
