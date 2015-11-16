import requests
from flask import Blueprint, redirect, session, url_for, request, abort
from flask.ext.login import LoginManager, login_user, logout_user
from server.core.models import User


login_manager = LoginManager()
auth_bp = Blueprint('auth_bp', __name__, template_folder='templates')


@auth_bp.route('/logout')
def logout():
    session.pop('access_token', None)
    logout_user()
    return redirect(url_for('core.index'))


# Authorization via login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
