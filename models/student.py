#!/usr/bin/python3
"""
Student Module
"""

from models.base_model import BaseModel, Base
from models.building import Building
from sqlalchemy import Column, String, ForeignKey, CHAR, UniqueConstraint
from sqlalchemy.orm import relationship

class Student(BaseModel, Base):
    __tablename__ = "students"
    Student_name = Column(String(128), nullable=True)
    Student_ID = Column(String(128), nullable=True)
    Country = Column(String(128), nullable=True)
    Room_ID = Column(CHAR(10), ForeignKey("buildings.room_id", ondelete="CASCADE"), nullable=False)
    Zone = Column(CHAR(1), nullable=True)

    rooms = relationship("Building", back_populates="students")

    __table_args__ = (
        UniqueConstraint('Country', 'Room_ID', name='uq_country_room'),
        UniqueConstraint('Zone', 'Room_ID', name='uq_zone_room')
    )
