#!/usr/bin/env python3
"""Construct the core application"""
from flask import Flask

from har_restapi.config import Config
from har_restapi.models import db
from har_restapi.routes import init_app


def create_app():
    """Construct the core application

    Returns:
        flask.app.Flask
    """
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    # Prepare the application to work with SQLAlchemy
    db.init_app(app)

    # Take care of both setUp and TearDown
    with app.app_context():
        # Initialize Plugins
        init_app(app)
    return app
