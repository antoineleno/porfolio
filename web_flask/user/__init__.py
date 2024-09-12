#!/usr/bin/python3
"""Init module"""

import os
import sys
from flask import Blueprint



app_views_user = Blueprint('app_views_user', __name__, url_prefix='/campusstay', template_folder='templates', static_folder='static')

from user.student_user import *
