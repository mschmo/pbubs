from flask_oauth import OAuth


oauth = OAuth()


class OAuthSignIn:

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']


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