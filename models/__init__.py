#!/usr/bin/python3
"""__init_ module
"""

from os import getenv
from models.engine.db_storage import DBStorage

"""TypeStorage = getenv("CAMPUS_TYPE_STORAGE")

if TypeStorage == "db":"""
storage = DBStorage()
storage.reload()
