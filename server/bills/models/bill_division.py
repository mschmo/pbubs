from server.db import db, ActiveModel


class BillDivision(ActiveModel, db.Model):
    __tablename__ = 'bill_divisions'

    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    payed = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return '<Bill Division bill_id={}, user_id={}>'.format(self.bill_id, self.user_id)
