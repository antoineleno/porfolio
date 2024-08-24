#!/usr/bin/python3
"""init module"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/campus/admin', template_folder='templates', static_folder='static')


from dashborad.dashboard import *
