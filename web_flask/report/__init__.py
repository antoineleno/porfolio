#!/usr/bin/python3
"""init module"""
from flask import Blueprint


app_views_report = Blueprint('app_views_report', __name__, url_prefix='/campusstay/admin', template_folder='templates', static_folder='static')


from report.report import *
