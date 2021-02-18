from flask import Flask
# from flasgger import Swagger

from flask_mongoengine import MongoEngine
from mongoengine import DoesNotExist

from celery.utils.log import get_task_logger

from src.config import ConfigFlask, ConfigMongoDB, ConfigCelery, make_celery

# Configs flask backend and mongodb
app = Flask(ConfigFlask.APP_NAME)
app.config.from_object(ConfigFlask)

# # Swagger
# template = {
#   "swagger": "2.0",
#   "info": {
#     "title": "s0nar API",
#     "description": "s0nar API",
#     "contact": {
#       "responsibleOrganization": "ME",
#       "responsibleDeveloper": "Me",
#       "email": "me@me.com",
#       "url": "www.me.com",
#     }
#   },
#   #"host": "s0nar",  # overrides localhost:500
#   #"basePath": "/api",  # base bash for blueprint registration
#   "schemes": [
#     "http",
#     "https"
#   ],
#   "securityDefinitions": {
#     "ApiKeyAuth": {
#       "type": "apiKey",
#       "in": "header",
#       "name": "x-api-key"
#     }
#   },
#   "security": {
#     "basicAuth": []
#   }
# }
# swagger = Swagger(app, template=template)

# Gets mongodb connection
db = MongoEngine()
db.init_app(app)

# Sets Celery config
app.config.from_object(ConfigCelery)
celery_app = make_celery(app)
celery_logger = get_task_logger(__name__)

# --------------------------
# Register all blueprints
# --------------------------
from src.blueprints.dataset_blueprint import dataset_blueprint
from src.blueprints.model_blueprint import model_blueprint
from src.blueprints.anomalies_blueprint import anomaly_blueprint

app.register_blueprint(dataset_blueprint)
app.register_blueprint(model_blueprint)
app.register_blueprint(anomaly_blueprint)

# --------------------------
# Error handlers
# --------------------------
@app.errorhandler(DoesNotExist)
def handle_not_found_error(ex):
    app.logger.error(ex)
    return 'Not Found', 404


@app.errorhandler(500)
def handle_internal_error(ex):
    app.logger.error(ex)
    return 'Internal Error', 500


@app.errorhandler(400)
def handle_internal_error(ex):
    app.logger.error(ex)
    return 'Bad Request', 400
