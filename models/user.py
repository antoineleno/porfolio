#!/usr/bin/python3
"""user module"""
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel, Base, UserMixin):
    """User class"""
    __tablename__ = "users"
    full_name = Column(String(256), nullable=False)
    username = Column(String(128), nullable=False)
    email = Column(String(250), nullable=True)
    department = Column(String(100), nullable=True)
    password_hash = Column(String(128), nullable=False)


    @property
    def password(self):
        raise AttributeError('Password is not a readable Attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password=password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password=password)

    def __str__(self):
        return '<User %r>' % User.id
