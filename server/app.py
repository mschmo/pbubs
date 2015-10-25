import requests
from flask import Flask, redirect, url_for, session, abort
from server.db import db
from server.oauth import configure_oauth
from server.models.accepted_emails import AcceptedEmail


app = Flask(__name__)
app.config.from_pyfile('config_default.py')
app.config.from_pyfile('config_local.py', silent=True)
configure_oauth(app)
db.init_app(app)


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

    if not AcceptedEmail.validate_oauth_resp(user_data):
        abort(403)

    return user_data['email']
