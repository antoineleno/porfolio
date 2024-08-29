#!/usr/bin/python3
"""Init module"""

import os
import sys
from flask import Blueprint


base_path = os.path.dirname(__file__)
parent_path = os.path.abspath(os.path.join(base_path, '../../'))
sys.path.append(parent_path)

app_views_dashboard = Blueprint(
    'app_views_dashboard',
    __name__,
    url_prefix='/campusstay',
    template_folder='templates',
    static_folder='static'
)

from dashboard.dashboard import *
