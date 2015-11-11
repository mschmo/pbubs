from server.db import db, ActiveModel


class BillType(ActiveModel, db.Model):
    __tablename__ = 'bill_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<Bill Type {}>'.format(self.name)
