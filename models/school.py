#!/usr/bin/python3
"""
School Module
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer



class School(BaseModel, Base):
    """Student class"""
    __tablename__ = "schools"
    school_id = Column(Integer, primary_key=True, autoincrement=True)
    school_name = Column(String(128), nullable=True, unique=True)
    school_dean = Column(String(128), nullable=True)
    email = Column(String(128), nullable=True)

