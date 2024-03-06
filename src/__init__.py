from flask import Flask

from src.extensions import db
from .routes.main import main
from .routes.api import api

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hoga.sqlite3'

    db.init_app(app)

    from . import models

    with app.app_context():
        db.create_all()
    app.register_blueprint(main)
    app.register_blueprint(api)

    return app
