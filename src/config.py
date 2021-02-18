from celery import Celery

from src.environment import env


class ConfigMongoDB(object):
    MONGODB_DB = env.str('MONGODB_INIT_DB_DATABASE')
    MONGODB_HOST = env.str('MONGODB_HOST')
    MONGODB_PORT = env.int('MONGODB_CONTAINER_PORT')
    MONGODB_USERNAME = env.str('MONGODB_USER')
    MONGODB_PASSWORD = env.str('MONGODB_PASSWORD')
    MONGODB_AUTH_SOURCE = env.str('MONGODB_AUTH_SOURCE')


class ConfigAWSs3(object):
    ACCESS_KEY = env.str('AWS_ACCESS_KEY')
    SECRET_KEY = env.str('AWS_SECRET_KEY')
    WIPER_BUCKET = env.str('AWS_WIPER_BUCKET')
    MODELS_FOLDER = env.str('AWS_MODELS_FOLDER')
    DATASETS_FOLDER = env.str('AWS_DATASETS_FOLDER')


class ConfigFlask(object):
    APP_NAME = env.str('APP_NAME')
    DEBUG = env.bool('APP_DEBUG')
    CSRF_ENABLED = env.bool('APP_CSRF_ENABLED')
    HOST = env.str('APP_HOST')
    PORT = env.str('APP_CONTAINER_PORT')
    UPLOAD_FOLDER = env.str('APP_UPLOAD_FOLDER')
    API_KEY = env.str('APP_API_KEY')
    MONGODB_SETTINGS = {
        'db': ConfigMongoDB.MONGODB_DB,
        'host': ConfigMongoDB.MONGODB_HOST,
        'port': ConfigMongoDB.MONGODB_PORT,
        'username': ConfigMongoDB.MONGODB_USERNAME,
        'password': ConfigMongoDB.MONGODB_PASSWORD,
        'authentication_source': ConfigMongoDB.MONGODB_AUTH_SOURCE
    }


class ConfigCelery(object):
    CELERY_RESULT_BACKEND = 'rpc://'
    CELERY_BROKER_URL = 'amqp://{0}:{1}@{2}:{3}/{4}'.format(
        env.str('RABBITMQ_DEFAULT_USER'),
        env.str('RABBITMQ_DEFAULT_PASS'),
        env.str('RABBITMQ_HOST'),
        env.str('RABBITMQ_CONTAINER_PORT'),
        env.str('RABBITMQ_DEFAULT_VHOST')
    )


def make_celery(app):
    """
    Setup Celery app

    :param app: flask app

    :return: Celery object
    """
    celery = Celery(app.import_name,
                    backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(
        CELERY_TASK_SERIALIZER='json',
        CELERY_RESULT_SERIALIZER='json',
        CELERY_ACCEPT_CONTENT=['json'],
        CELERY_TIMEZONE='Europe/Madrid',
        CELERY_ENABLE_UTC=True
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
