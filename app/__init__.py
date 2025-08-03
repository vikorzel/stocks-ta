from flask import Flask
from . import routes
from . import config
import os

def create_app():
    config_data = config.get_app_config()
    print(f"Running TA App version: {config_data['version']}")
    app = Flask(__name__, static_folder=config_data['static_folder'], template_folder=config_data['template_folder'])
    routes.init_routes(app, config_data)
    return app