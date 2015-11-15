from datetime import datetime
from server.db import db, ActiveModel


class Bill(ActiveModel, db.Model):
    __tablename__ = 'bills'

    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('bill_types.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.String(128), unique=True, nullable=False)
    amount = db.Column(db.DECIMAL(5, 2), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    bill_type = db.relationship('BillType', foreign_keys='Bill.type_id', uselist=False, backref='events')

    @property
    def pretty_date(self):
        return self.created_at.strftime('%b %d, %Y')

    @classmethod
    def create_bill(cls, form, user_id):
        bill = cls(
            type_id=form.bill_type.data,
            user_id=user_id,
            comment=form.comment.data,
            amount=form.amount.data,
            created_at=datetime.now()
        )
        bill.save()
        return bill

    def __repr__(self):
        return '<Bill {}>'.format(self.id)
