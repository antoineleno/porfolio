#!/usr/bin/python3
"""Facility module"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.building import room_facility


class Facility(BaseModel, Base):
    __tablename__ = "facilities"
    name = Column(String(128), nullable=False)
    room_facilities = relationship("Building", secondary=room_facility, back_populates="facilities")
