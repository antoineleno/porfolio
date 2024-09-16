#!/usr/bin/python3
"""
FORM module
"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField
from wtforms import PasswordField, EmailField, BooleanField
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired, length, NumberRange
from flask_wtf.file import FileField, FileRequired


class LoginForm(FlaskForm):
    """Login form"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Enter Your Password',
                             validators=[DataRequired()])
    submit = SubmitField('Log in')


class PasswordChangeForm(FlaskForm):
    """Password change"""
    current_password = PasswordField('Current Password',
                                     validators=[DataRequired(),
                                                 length(min=6)])
    new_password = PasswordField('New Password',
                                 validators=[DataRequired(), length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password',
                                         validators=[DataRequired(),
                                                     length(min=6)])
    change_password = SubmitField('Change Password')
