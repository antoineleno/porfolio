#!/usr/bin/python3
"""Base_model module"""

from uuid import uuid4
from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel:
    """BaseModel class: to serve for parent class for all the classes"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False,default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Constructor class"""
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    time_format = "%Y-%m-%dT%H:%M:%S.%f"
                    if key == 'created_at':
                        value = datetime.strptime(value, time_format)
                        setattr(self, key, value)
                    elif key == 'updated_at':
                        value = datetime.strptime(value, time_format)
                        setattr(self, key, value)
                    setattr(self, key, value)
        
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self):
        """Method to return the representation of an object"""
        return "[{}] ({}) {}".format(type(self).__name__,
                                     self.id, self.__dict__)

    def save(self):
        """Method to save an object to a file or database"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Method to returned the dictionary representation of an object"""
        dict = self.__dict__
        if 'created_at' in dict.keys() \
                and isinstance(dict['created_at'], datetime):
            dict['created_at'] = dict['created_at'].isoformat()

        if 'updated_at' in dict.keys() \
                and isinstance(dict['updated_at'], datetime):
            dict['updated_at'] = dict['updated_at'].isoformat()
            dict['__class__'] = type(self).__name__
            return dict