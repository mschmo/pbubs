import requests
from flask import Flask, redirect, url_for, session, abort, request, render_template
from flask.ext.login import LoginManager, login_user, logout_user, login_required
from server.db import db
from server.oauth import configure_oauth
from server.models import User


app = Flask(__name__)
app.config.from_pyfile('config_default.py')
app.config.from_pyfile('config_local.py', silent=True)
configure_oauth(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))

    access_token = access_token[0]
    headers = {'Authorization': 'OAuth {}'.format(access_token)}
    req = requests.get('https://www.googleapis.com/oauth2/v1/userinfo', headers=headers)
    user_data = req.json()
    if user_data.get('error'):
        if user_data['error']['code'] == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('login'))

    user = User.get_or_create_user(user_data)
    if not user:
        abort(403)

    remember_me = session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.values.get('state') or url_for('dash'))


@app.route('/dash')
@login_required
def dash():
    return render_template('base.html')


@app.route('/profile/<int:user_id>')
@login_required
def user_profile(user_id):
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)


@app.route('/logout')
def logout():
    session.pop('access_token', None)
    logout_user()
    return redirect(url_for('index'))


# Authorization via login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
