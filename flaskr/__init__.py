import os

from flask import Flask, request
from . import db, appointment

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    """Register command to initialize the DB and ask app to close connection upon app closure"""
    db.init_app(app)

    """Register commands to create and get appointments"""
    app.register_blueprint(appointment.bp)

    return app