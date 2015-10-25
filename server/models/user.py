from datetime import datetime
from server.db import db, ActiveModel
from server.models import AcceptedEmail


class User(ActiveModel, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    avatar_url = db.Column(db.String(1024), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @classmethod
    def get_or_create_user(cls, oauth_response):
        # Verify that email has been approved
        if not AcceptedEmail.validate_oauth_resp(oauth_response):
            return

        user = cls.query.filter(cls.email == oauth_response['email']).first()
        if not user:
            user = cls()
            user.first_name = oauth_response['given_name']
            user.last_name = oauth_response['family_name']
            user.email = oauth_response['email']
            user.avatar_url = oauth_response['picture']
            user.save()
        return user

    def __repr__(self):
        return '<User {}>'.format(self.email)
