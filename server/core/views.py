from flask import render_template
from flask.ext.login import login_required

from server.core import core
from server.core.models import User


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
