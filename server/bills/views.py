from flask import render_template, url_for, redirect
from flask.ext.login import login_required, current_user

from server.bills import bills
from server.bills.forms import BillForm
from server.bills.models import Bill, BillDivision
from server.core.models import User


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
        users_to_pay = []
        selected_users = form.users_to_pay.data
        if type(selected_users) == list:
            users_to_pay += form.users_to_pay.data
        elif type(selected_users) == int:
            users_to_pay.append(selected_users)
        if form.include_myself:
            users_to_pay.append(current_user.id)
        BillDivision.add_new_divisions(bill, users_to_pay)
        return redirect(url_for('.view_bill', bill_id=bill.id))
    return render_template('bills/new_bill.html', form=form)


@bills.route('/<int:bill_id>')
@login_required
def view_bill(bill_id):
    bill = Bill.query.get(bill_id)
    return render_template('bills/view_bill.html', bill=bill)


@bills.route('/user')
@bills.route('/user/<int:user_id>')
@login_required
def user_bills(user_id=None):
    if not user_id:
        user_id = current_user.id
    divisions_to_pay = BillDivision.get_user_bills_to_pay(user_id)
    bills_posted = Bill.query.filter(Bill.user_id==user_id).all()
    divisions_paid = BillDivision.query.filter(BillDivision.user_id==user_id, BillDivision.payed==1).all()
    user = User.query.get(user_id)
    return render_template('bills/user_bills.html',
                           divisions_to_pay=divisions_to_pay,
                           bills_posted=bills_posted,
                           divisions_paid=divisions_paid,
                           user=user)
