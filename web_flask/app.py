#!/usr/bin/python3
"""
APP module
"""
from flask_cors import CORS
from flask import Flask
from dashboard import app_views_dashboard
from hostels import app_views_male
from hostels import app_views_female
from search import app_views_search
from inquiries import app_views_inquiries
from report import app_views_report
from leaves import app_views_leaves
from flask_login import LoginManager
from auth import app_views_auth
from user import app_views_user
from models import storage


app = Flask(__name__)
CORS(app, resources={r'/campusstay/*': {'origins': '0.0.0.0'}})

app.secret_key = "a2cf8cf6ad37b0d8eb2b51846aee0e34"
app.config['UPLOAD_FOLDER'] = 'dashboard/static/img'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = {'png'} 


app.register_blueprint(app_views_dashboard)
app.register_blueprint(app_views_male)
app.register_blueprint(app_views_female)
app.register_blueprint(app_views_search)
app.register_blueprint(app_views_inquiries)
app.register_blueprint(app_views_report)
app.register_blueprint(app_views_leaves)
app.register_blueprint(app_views_auth)
app.register_blueprint(app_views_user)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'app_views_auth.login'


@login_manager.user_loader
def load_user(id):
    """Load current user session"""
    return storage.get_user_object(id)


@app.teardown_appcontext
def teardown_db(exception):
    """Close everytime the opened session"""
    storage.close()


if __name__ == "__main__":
    app.run(debug=True)
