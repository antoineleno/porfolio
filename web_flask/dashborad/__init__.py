#!/usr/bin/python3
"""init module"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/campus/admin')

from dashborad.dashboard import *
