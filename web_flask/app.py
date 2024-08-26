#!/usr/bin/python3
"""
APP module
"""
from flask_cors import CORS
from flask import Flask
from dashboard import app_views_dashboard
from male import app_views_male
from female import app_views_female
from search import app_views_search
from inquiries import app_views_inquiries
from report import app_views_report
from leaves import app_views_leaves



app = Flask(__name__)
CORS(app, resources={r'/campusstay/*': {'origins': '0.0.0.0'}})

app.register_blueprint(app_views_dashboard)
app.register_blueprint(app_views_male)
app.register_blueprint(app_views_female)
app.register_blueprint(app_views_search)
app.register_blueprint(app_views_inquiries)
app.register_blueprint(app_views_report)
app.register_blueprint(app_views_leaves)

if __name__ == "__main__":
    app.run(debug=True)
