__version__ = '1.0.0'

import logging.config
import os
from pathlib import Path

import yaml
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint


def get_scheme(swagger_yml):
    """
    Gets the schema to be presented by the Swagger.
    Args:
        swagger_yml (dict): Swagger settings in a dictionary.
    """
    try:
        swagger_yml['schemes'] = [os.environ['SCHEMES']]
        logging.getLogger('controller.api').info("SCHEMES > OK")
    except KeyError:
        logging.getLogger('controller.api').info('SCHEMES > not found')


def create_app():
    """
     Create the Flask application, prepare the log configurations,
     Swagger and add the api endpoints.
    """
    root_path, path = Path(__file__).parents[0], ''
    app = Flask(__name__)
    '''
    It is assumed that the root_path/'config' directory exists.
    It must contain the following files:
        - config.py
        - logging.yaml
        - logging_cloud.yaml
        - swagger.yaml
    '''
    root_path = root_path / 'config'
    # logging configs
    if os.environ.get('MODE') == 'prod':
        path = root_path / 'logging_cloud.yaml'
    elif os.environ.get('MODE') == 'dev':
        print('----- STARTING DEVELOPMENT APPLICATION -----')
        if not os.path.exists('/var/log/'):
            print('WARNING: Logging not work, /var/log/ do not exist.')
        else:
            path = root_path / 'logging.yaml'

    if path:
        with open(str(path), 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    """
    Creates API docs endpoint from swagger file
    """
    doc_path = str(root_path / 'swagger.yaml')
    swagger_yml = yaml.safe_load(open(doc_path, 'r'))
    # Get scheme
    get_scheme(swagger_yml)
    # Register Swagger UI.
    app.register_blueprint(get_swaggerui_blueprint('/docs', doc_path, config={
        'spec': swagger_yml}), url_prefix='/docs')
    """
    Add the application endpoints.
    """
    # helpers controller
    from api_controller.controller.metrics_controller import metrics
    app.register_blueprint(metrics)
    # Start controller
    from api_controller.controller.start_controller import start
    app.register_blueprint(start)
    # face detect controller
    from api_controller.controller.face_detect_controller import \
        face_detect
    app.register_blueprint(face_detect)
    # face identify controller
    from api_controller.controller.face_identify_controller import \
        face_identify
    app.register_blueprint(face_identify)
    # face compare controller
    from api_controller.controller.face_compare_controller import \
        face_compare
    app.register_blueprint(face_compare)
    # Logger Init App.
    logging.getLogger('nearest_person.init').info('App created, ready to up.')
    return app
