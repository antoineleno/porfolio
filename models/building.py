from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
import uuid


def generate_short_uuid():
    """Generate a 10-character alphanumeric UUID."""
    return str(uuid.uuid1()).replace('-', '')[:10]


# Association table for many-to-many relationship
room_facility = Table('room_facility', Base.metadata,
    Column('room_id', String(60), ForeignKey('buildings.room_id'), nullable=False),
    Column('facility_id', String(60), ForeignKey('facilities.id'), nullable=False)
)


class Building(BaseModel, Base):
    """Building

    Args:
        BaseModel (class): base_model classs
        Base (instance): instance of declarative_base
    """
    __tablename__ = "buildings"
    hostel_id = Column(Integer, ForeignKey("hostels.hostel_id", ondelete="CASCADE"))
    block_name = Column(String(128), nullable=False)
    room_id = Column(String(60), primary_key=True, default=generate_short_uuid, unique=True, nullable=False)
    room_number = Column(String(128), unique=True)
    hostel = relationship("Hostel", back_populates="buildings")
    students = relationship("Student", back_populates="building", cascade="all, delete-orphan")
    facilities = relationship("Facility", secondary=room_facility, back_populates="room_facilities")
