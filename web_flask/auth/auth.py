#!/usr/bin/python3
"""
AUTH module
"""
from flask import Blueprint, render_template, flash, redirect, request
from .forms import LoginForm, PasswordChangeForm

from flask_login import login_user, login_required, logout_user
from auth import app_views_auth
from models import storage

auth = Blueprint('auth', __name__)


@app_views_auth.route('/login', methods=['GET', 'POST'])
def login():
    """Login method"""
    form = LoginForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            user = storage.get_user(username)

            if user:
                if user.verify_password(password=password):
                    first_user = storage.get_first_user()[0]
                    if storage.get_user(username).id == first_user:
                        login_user(user)
                        return redirect('/campusstay/admin/dashboard')
                    else:
                        login_user(user)
                        return redirect('/campusstay/user/home')
                else:
                    flash('Incorrect username or Password')

            else:
                message = """Account does not exist please ask the 
                administrator to create your account
                """
                flash(message)

    return render_template('login.html', form=form)


@app_views_auth.route('/logout', methods=['GET', 'POST'])
@login_required
def log_out():
    """Log user out"""
    form = LoginForm()
    logout_user()
    return render_template('login.html', form=form)

