from datetime import datetime
from flask import render_template, url_for, redirect
from flask.ext.login import login_required, current_user

from server.bills import bills
from server.bills.forms import BillForm
from server.bills.models import Bill


@bills.route('/')
@login_required
def view_all():
    return render_template('bills/view_bill.html', bill=Bill.query.all())


@bills.route('/new', methods=['GET', 'POST'])
@login_required
def new_bill():
    form = BillForm()
    form.add_select_options(current_user.id)
    if form.validate_on_submit():
        bill = Bill(
            type_id=form.bill_type.data,
            user_id=current_user.id,
            comment=form.comment.data,
            amount=form.amount.data,
            created_at=datetime.now()
        )
        bill.save()
        return redirect(url_for('.view_bill', bill_id=bill.id))
    return render_template('bills/new_bill.html', form=form)


@bills.route('/<int:bill_id>')
@login_required
def view_bill(bill_id):
    bill = Bill.query.get(bill_id)
    return render_template('bills/view_bill.html', bill=bill)
