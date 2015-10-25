import requests
from flask import Flask, redirect, url_for, session
from server.oauth import configure_oauth


app = Flask(__name__)
app.config.from_pyfile('config_default.py')
app.config.from_pyfile('config_local.py', silent=True)
configure_oauth(app)


@app.route('/')
def index():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))

    access_token = access_token[0]
    from urllib2 import Request, urlopen, URLError

    headers = {'Authorization': 'OAuth {}'.format(access_token)}
    req = requests.get('https://www.googleapis.com/oauth2/v1/userinfo', headers=headers)
    try:
        res = urlopen(req)
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('login'))
        return res.read()
    except:
        abort(500)

    return res.read()

