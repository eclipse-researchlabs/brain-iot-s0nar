import os

import boto3

from enum import Enum
from pathlib import Path
from src import app
from src.config import ConfigAWSs3
from urllib.parse import urlparse


s3 = boto3.client('s3', aws_access_key_id=ConfigAWSs3.ACCESS_KEY, aws_secret_access_key=ConfigAWSs3.SECRET_KEY)


class FileType(Enum):
    DATASET = 0
    ARIMA_BIN = 1
    TENSORFLOW_BIN = 2
    TENSORFLOW_JSON = 3


def _get_folder_by_type(file_type):
    """
    Get the Amazon's s3 bucket for any file_type

    :param file_type: which represents the file

    :return: Amazon's s3 bucket which correspond with file_type
    :raise: Exception when file type does not match with any FileType
    """
    if file_type == FileType.DATASET:
        return 'dataset'
    elif file_type == FileType.ARIMA_BIN:
        return 'models/arima'
    elif file_type == FileType.TENSORFLOW_BIN:
        return 'models/tensorflow/weight'
    elif file_type == FileType.TENSORFLOW_JSON:
        return 'models/tensorflow/info'
    raise Exception('Invalid file type')


def save_file_in_s3(file_path, file_type, file_name=None):
    """
    Save related s0nar files in S3 bucket

    :param file_path: where the file is local save
    :param file_type: the file type to get the path of S3 bucket
    :param file_name: the name that file received that will received in Bucket

    :return: S3 uri
    """
    file_name = os.path.basename(file_path) if file_name is None else file_name
    s3_file = '{}/{}'.format(_get_folder_by_type(file_type), file_name)
    s3.upload_file(file_path, ConfigAWSs3.WIPER_BUCKET, s3_file)

    app.logger.info("Upload Successful")
    return 's3://{}/{}'.format(ConfigAWSs3.WIPER_BUCKET, s3_file)


def retrieve_file_from_s3(s3_uri, file_name, file_type):
    """
    Download files from s3 bucket

    :param s3_uri: where is persisted the file
    :param file_name: name that file will received when its downloaded
    :param file_type: file type to get the Bucket's folder

    :return: local file path
    """
    folder = _get_folder_by_type(file_type)
    Path('/tmp/{}'.format(folder)).mkdir(parents=True, exist_ok=True)
    local_path = '/tmp/{}/{}'.format(folder, file_name)
    r = urlparse(s3_uri)
    bucket = r.netloc
    path = r.path[1:]
    s3.download_file(bucket, path, local_path)

    app.logger.info("{} retrieved".format(file_name))
    return local_path
