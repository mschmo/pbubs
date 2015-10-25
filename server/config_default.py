DEBUG = True
SECRET_KEY = 'development key'

# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console
GOOGLE_CLIENT_ID = '<Client-ID>'
GOOGLE_CLIENT_SECRET = '<Client-secret>'

# MySQL SQL-Alchemy set up
SQLALCHEMY_DATABASE_URI = 'mysql://local:local@127.0.0.1:3306/catherine'
SQLALCHEMY_MANAGE_DATABASE_URI = 'mysql://local:local@127.0.0.1:3306'