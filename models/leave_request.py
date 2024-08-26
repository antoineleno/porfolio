"""leave_request class"""
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import uuid
from models.student import Student


def generate_short_uuid():
    """Generate a 10-character alphanumeric UUID."""
    return str(uuid.uuid1())


class Leave(BaseModel, Base):
    """LEAVE

    Args:
        BaseModel (class): base_model classs
        Base (instance): instance of declarative_base
    """
    __tablename__ = "leaves"
    leave_id = Column(String(60), primary_key=True,
                      default=generate_short_uuid,
                      unique=True, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    description = Column(String(1000), nullable=False)
    place = Column(String(80), nullable=False)
    c_school = Column(String(10))
    c_sa = Column(String(10))
    status = Column(String(45))
    overstay = Column(String(45))
    date_out = Column(DateTime)
    date_in = Column(DateTime)
    student_id = Column(String(60), ForeignKey("students.Student_ID"),
                        nullable=False)
    student = relationship("Student", back_populates="leave")
