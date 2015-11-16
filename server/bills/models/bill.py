import urllib
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

    bill_type = db.relationship('BillType', foreign_keys='Bill.type_id', uselist=False, backref='bills')
    user = db.relationship('User', foreign_keys='Bill.user_id', uselist=False, backref='bills')

    @property
    def pretty_date(self):
        return self.created_at.strftime('%b %d, %Y')

    @property
    def venmo_note(self):
        return '{} Bill'.format(self.bill_type.name)

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

    def venmo_link(self):
        params = urllib.urlencode({
            'recipients': self.user.venmo_account,
            'amount': self.division_amount(),
            'note': self.venmo_note,
            'audience': 'public'
        })
        return 'https://venmo.com/?txn=pay&{}'.format(params)

    def division_amount(self):
        from server.bills.models import BillDivision
        return self.amount / BillDivision.query.filter(BillDivision.bill_id==self.id).count()

    def is_paid(self):
        from server.bills.models import BillDivision
        return all([division.payed for division in BillDivision.query.filter(BillDivision.bill_id==self.id).all()])

    def __repr__(self):
        return '<Bill {}>'.format(self.id)
