#!/usr/bin/python3
"""init module"""
from flask import Blueprint


app_views_leaves = Blueprint('app_views_leaves', __name__, url_prefix='/campusstay', template_folder='templates', static_folder='static')


from leaves.leaves import *
