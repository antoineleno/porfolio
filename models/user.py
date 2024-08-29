#!/usr/bin/python3
"""user module"""
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column


class User(BaseModel, Base):
    __tablename__ = "users"
    full_name = Column(String(256), nullable=False)
    user_name = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    role = Column(String(20), nullable=False)
