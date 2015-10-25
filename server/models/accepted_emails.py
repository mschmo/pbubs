from server.db import db, ActiveModel


class AcceptedEmail(ActiveModel, db.Model):
    __tablename__ = 'accepted_emails'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)