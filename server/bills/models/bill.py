from datetime import datetime
from server.db import db, ActiveModel


class Bill(ActiveModel, db.Model):
    __tablename__ = 'bills'

    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(128), unique=True, nullable=False)
    amount = db.Column(db.DECIMAL(5, 2), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @property
    def pretty_date(self):
        return self.created_at.strftime('%b %d, %Y')

    def __repr__(self):
        return '<Bill {}>'.format(self.id)
