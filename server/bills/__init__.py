from flask import Blueprint


bills = Blueprint('bills', __name__, template_folder='templates')

from .views import *
