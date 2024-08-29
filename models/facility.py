"""Facility module"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class Facility(BaseModel, Base):
    __tablename__ = "facilities"
    id = Column(String(60), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(128), nullable=False)
    room_facilities = relationship("Building", secondary="room_facility", back_populates="amenities")
