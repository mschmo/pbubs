from flask import Flask, render_template
from flask.ext.login import login_required
from flask.ext.migrate import Migrate
from server.db import db
from server.oauth import configure_oauth
from server.models import User


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config_default.py')
    app.config.from_pyfile('config_local.py', silent=True)
    Migrate(app, db)
    configure_oauth(app)
    db.init_app(app)

    from auth import auth_bp, login_manager
    login_manager.init_app(app)
    app.register_blueprint(auth_bp)

    @app.route('/dash')
    @login_required
    def dash():
        news_feed = []
        return render_template('dash.html', news_feed=news_feed)


    @app.route('/profile/<int:user_id>')
    @login_required
    def user_profile(user_id):
        user = User.query.get(user_id)
        return render_template('profile.html', user=user)

    return app