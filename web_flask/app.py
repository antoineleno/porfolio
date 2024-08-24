#!/usr/bin/python3
"""
API module
"""

from flask import Flask
from dashborad import app_views
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r'/campus/admin/*': {'origins': '0.0.0.0'}})

app.register_blueprint(app_views)

if __name__ == "__main__":
    app.run(debug=True)
