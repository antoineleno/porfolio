#!/usr/bin/python3
"""
Maintenance Module
"""

from models.base_model import BaseModel, Base
from models.student import Student
from sqlalchemy import Column, String, ForeignKey


class Maintenance(BaseModel, Base):
    """Maintenace Class"""
    __tablename__ = "maintenances"
    student_id = Column(String(60),
                     ForeignKey("students.Student_ID",
                                ondelete="CASCADE"), nullable=False)
    status = Column(String(20), nullable=True)
    amenity = Column(String(60))
    description = Column(String(450), nullable=False)
