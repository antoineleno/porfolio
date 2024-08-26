#!/usr/bin/python3
"""init module"""
from flask import Blueprint


app_views_inquiries = Blueprint('app_views_inquiries', __name__, url_prefix='/campusstay/admin', template_folder='templates', static_folder='static')


from inquiries.inquiries import *
