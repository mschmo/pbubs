import requests
from flask import Blueprint, redirect, session, url_for, request, abort
from flask.ext.login import LoginManager, login_user, logout_user
from server.models import User


login_manager = LoginManager()
auth_bp = Blueprint('auth_bp', __name__, template_folder='templates')


@auth_bp.route('/')
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


@auth_bp.route('/logout')
def logout():
    session.pop('access_token', None)
    logout_user()
    return redirect(url_for('auth_bp.index'))


# Authorization via login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
