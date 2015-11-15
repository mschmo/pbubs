from flask import render_template, url_for, redirect
from flask.ext.login import login_required, current_user

from server.bills import bills
from server.bills.forms import BillForm
from server.bills.models import Bill, BillDivision


@bills.route('/')
@login_required
def view_all():
    return render_template('bills/view_all.html', bills=Bill.query.all())


@bills.route('/new', methods=['GET', 'POST'])
@login_required
def new_bill():
    form = BillForm()
    form.add_select_options(current_user.id)
    if form.validate_on_submit():
        bill = Bill.create_bill(form, current_user.id)
        users_to_pay = form.users_to_pay.data
        if form.include_myself and users_to_pay:
            users_to_pay.append(current_user.id)
        BillDivision.add_new_divisions(bill, users_to_pay, form.include_myself)
        return redirect(url_for('.view_bill', bill_id=bill.id))
    return render_template('bills/new_bill.html', form=form)


@bills.route('/<int:bill_id>')
@login_required
def view_bill(bill_id):
    bill = Bill.query.get(bill_id)
    return render_template('bills/view_bill.html', bill=bill)
