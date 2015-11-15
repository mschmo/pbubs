from flask_wtf import Form
from wtforms import StringField, DecimalField, SelectField
from wtforms.validators import DataRequired, Optional

from server.bills.models import BillType
from server.core.models import User


class BillForm(Form):
    bill_type = SelectField('Type', validators=[DataRequired()], coerce=int)
    comment = StringField('Comment', validators=[Optional()])
    amount = DecimalField('Amount', validators=[DataRequired()])
    users_to_pay = SelectField('Who Has To Pay', validators=[DataRequired()], coerce=int)

    def add_select_options(self):
        self.bill_type.choices = [(bt.id, bt.name) for bt in BillType.query.order_by('name')]
        self.users_to_pay.choices = [(user.id, user.name) for user in User.query.order_by('name')]
