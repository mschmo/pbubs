from flask import Flask
from flask.ext.migrate import Migrate
from server.db import db
from server.oauth import configure_oauth

# Blueprints
from server.auth import auth_bp, login_manager
from server.bills import bills
from server.core import core


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config_default.py')
    app.config.from_pyfile('config_local.py', silent=True)
    Migrate(app, db)
    configure_oauth(app)
    db.init_app(app)

    login_manager.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(bills)
    app.register_blueprint(core)

    return app
