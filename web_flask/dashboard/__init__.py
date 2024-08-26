#!/usr/bin/python3
"""init module"""
from flask import Blueprint


app_views_dashboard = Blueprint('app_views_dashboard', __name__, url_prefix='/campusstay', template_folder='templates', static_folder='static')


from dashboard.dashboard import *
