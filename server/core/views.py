import requests
from flask import render_template, session, redirect, url_for, abort, request
from flask.ext.login import login_required, login_user

from server.core import core
from server.core.models import User


@core.route('/')
def index():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('.landing'))

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
    return redirect(request.values.get('state') or url_for('.dash'))


@core.route('/landing')
def landing():
    return render_template('core/landing.html')


@core.route('/dash')
@login_required
def dash():
    news_feed = []
    return render_template('dash.html', news_feed=news_feed)


@core.route('/profile/<int:user_id>')
@login_required
def user_profile(user_id):
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)
