#!/usr/bin/python3
"""init module"""
from flask import Blueprint


app_views_search = Blueprint('app_views_search', __name__, url_prefix='/campusstay', template_folder='templates', static_folder='static')


from search.search import *
