#!/usr/bin/python3
"""hostel class"""
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship


class Hostel(BaseModel, Base):
    """Hostel class

    Args:
        BaseModel (class): Base model class
        Base (instance): Instance from declarative_base
    """
    __tablename__ = "hostels"
    hostel_id = Column(Integer, primary_key=True, autoincrement=True)
    hostel_type = Column(String(128), nullable=False)
    buildings = relationship("Building", back_populates="hostel",
                             cascade="all, delete-orphan")
