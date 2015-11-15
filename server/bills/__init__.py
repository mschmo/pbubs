from flask import Blueprint


bills = Blueprint('bills', __name__, template_folder='templates', url_prefix='/bills')

from .views import *
