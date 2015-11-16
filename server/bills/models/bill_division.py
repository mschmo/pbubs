from server.db import db, ActiveModel, full_commit
from server.core.models import User


class BillDivision(ActiveModel, db.Model):
    __tablename__ = 'bill_divisions'

    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey('bills.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    payed = db.Column(db.Boolean, nullable=False, default=False)

    bill = db.relationship('Bill', foreign_keys='BillDivision.bill_id', uselist=False, backref='divisions')

    @classmethod
    def add_new_divisions(cls, bill, users_to_pay=[], exclude=None):
        if not users_to_pay:
            users_to_pay = User.query
            if exclude is not None:
                users_to_pay = users_to_pay.filter(User.id!=exclude)
            users_to_pay = map(lambda x: x.id, users_to_pay.all())

        for user_id in users_to_pay:
            division = cls(bill_id=bill.id, user_id=user_id)
            division.save(commit=False)
        full_commit()

    @classmethod
    def get_user_bills_to_pay(cls, user_id):
        return cls.query.filter(cls.user_id==user_id, cls.payed==0).all()

    def __repr__(self):
        return '<Bill Division bill_id={}, user_id={}>'.format(self.bill_id, self.user_id)
