from flask import url_for, session, redirect
from flask_oauth import OAuth


oauth = OAuth()


def configure_oauth(app):
    google = oauth.remote_app('google',
                              base_url='https://www.google.com/accounts/',
                              authorize_url='https://accounts.google.com/o/oauth2/auth',
                              request_token_url=None,
                              request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                    'response_type': 'code'},
                              access_token_url='https://accounts.google.com/o/oauth2/token',
                              access_token_method='POST',
                              access_token_params={'grant_type': 'authorization_code'},
                              consumer_key=app.config['GOOGLE_CLIENT_ID'],
                              consumer_secret=app.config['GOOGLE_CLIENT_SECRET'])

    @app.route('/login')
    def login():
        callback = url_for('authorized', _external=True)
        return google.authorize(callback=callback)


    # Redirect
    @app.route('/oauth_redirect')
    @google.authorized_handler
    def authorized(resp):
        access_token = resp['access_token']
        session['access_token'] = access_token, ''
        return redirect(url_for('auth_bp.index'))

    @google.tokengetter
    def get_access_token():
        return session.get('access_token')