#!/usr/bin/python3
"""init module"""
from flask import Blueprint


app_views_auth = Blueprint('app_views_auth', __name__, url_prefix='/campusstay', template_folder='templates', static_folder='static')


from auth.auth import *
