#!/usr/bin/python3
"""init module"""
from flask import Blueprint


app_views_male = Blueprint('app_views_male', __name__, url_prefix='/campusstay', template_folder='templates', static_folder='static')
app_views_female = Blueprint('app_views_female', __name__, url_prefix='/campusstay', template_folder='templates', static_folder='static')


from hostels.hostels import *
