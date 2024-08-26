#!/usr/bin/python3
"""
Student Module
"""

from models.base_model import BaseModel, Base
from models.building import Building
from sqlalchemy import Column, String, ForeignKey, CHAR, UniqueConstraint
from sqlalchemy.orm import relationship


class Student(BaseModel, Base):
    """Student class"""
    __tablename__ = "students"
    Student_name = Column(String(128), nullable=True)
    Student_ID = Column(String(128), unique=True, nullable=True)
    Country = Column(String(128), nullable=True)
    Room_ID = Column(String(60),
                     ForeignKey("buildings.room_id",
                                ondelete="CASCADE"), nullable=False)
    Zone = Column(CHAR(1), nullable=False)
    building = relationship("Building", back_populates="students")
    leave = relationship("Leave", back_populates="student",
                         cascade="all, delete-orphan")

    """ __table_args__ = (
        UniqueConstraint('Country', 'Room_ID', name='uq_country_room'),
        UniqueConstraint('Zone', 'Room_ID', name='uq_zone_room')
    )
    """
