from server.db import db, ActiveModel


class AcceptedEmail(ActiveModel, db.Model):
    __tablename__ = 'accepted_emails'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)

    @classmethod
    def validate_oauth_resp(cls, user_data):
        return cls.query.filter(cls.email == user_data.get('email')).count()
