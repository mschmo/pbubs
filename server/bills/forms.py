from flask_wtf import Form
from wtforms import StringField, DecimalField, SelectField, BooleanField
from wtforms.validators import DataRequired, Optional

from server.bills.models import BillType
from server.core.models import User


class BillForm(Form):
    bill_type = SelectField('Type', validators=[DataRequired()], coerce=int)
    comment = StringField('Comment', validators=[Optional()])
    amount = DecimalField('Total Amount Due', validators=[DataRequired()])
    # Default to all tenants
    users_to_pay = SelectField('Who Has To Pay', validators=[Optional()], coerce=int)
    include_myself = BooleanField('Include Myself', validators=[Optional()], default='checked')

    def add_select_options(self, user_id):
        self.bill_type.choices = [(bt.id, bt.name) for bt in BillType.query.order_by('name')]
        self.users_to_pay.choices = [(user.id, user.full_name)
                                     for user in User.query.filter(User.id!=user_id).order_by('first_name')]
