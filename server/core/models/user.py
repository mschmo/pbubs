from datetime import datetime
from flask.ext.login import UserMixin
from server.db import db, ActiveModel
from server.auth.models import AcceptedEmail


class User(ActiveModel, UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    venmo_account = db.Column(db.String(64))
    avatar_url = db.Column(db.String(1024), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

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

    def has_unpaid_bills(self):
        from server.bills.models import BillDivision
        return BillDivision.query.filter(BillDivision.user_id==self.id, BillDivision.payed==0).count()

    def unpaid_due(self):
        from server.bills.models import BillDivision
        unpaid_divisions = BillDivision.query.filter(BillDivision.user_id==self.id, BillDivision.payed==0).all()
        return sum(map(lambda x: x.amount, unpaid_divisions))

    def is_active(self):
        return self.active

    def __repr__(self):
        return '<User {}>'.format(self.email)
