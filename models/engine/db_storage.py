#!/usr/bin/python3
"""
DB storage module
"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.building import Building
from models.user import User
from models.student import Student
from models.facility import Facility
from models.hostel import Hostel


class DBStorage:
    """DBStorage
    Class to manage objects storage to DB
    """
    __engine = None
    __session = None

    def __init__(self):
        """Contructor method
        """
        db_user = getenv("MYUSER")
        db_password = getenv("MYPWD")
        db_name = getenv("MYDB")
        host = getenv("MYHOST")
        env = getenv("CAMPUS_ENV")

        self.__engine = create_engine(
                    'mysql+mysqldb://{}:{}@{}/{}'
                    .format(db_user, db_password, host,
                            db_name), pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """all to retrieve all records from DB

        Args:
            cls (string, optional): Object to return. Defaults to None.

        Returns:
            Dict: All records from a database
        """
        allclasses = {"User": User,
                      "Building": Building,
                      "Student": Student,
                      "Facility": Facility,
                      "Hostel": Hostel
                      }
        obj_result = {}
        cls = cls if not isinstance(cls, str) else allclasses.get(cls)
        if cls is None:
            for cls in allclasses:
                objs = self.__session.query(cls).all()
                for obj in objs:
                    obj_result["{}.{}".format(obj.__table__, obj.id)] = obj
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                obj_result["{}.{}".format(obj.__table__, obj.id)] = obj
        return obj_result

    def new(self, obj):
        """new : to add an an obj to a session

        Args:
            obj (instance): Obj created to be addred
        """
        """if isinstance(obj, Student):
            existing_count = self.__session.query(Student).filter(Building.room_id == Student.Room_ID).count()
            if existing_count >= 4:
                raise ValueError("Room_ID usage limit exceeded")
            else:
                self.__session.add(obj)
        else:"""
        self.__session.add(obj)

    def save(self):
        """save: method to commit changes to a db
        """
        self.__session.commit()

    def delete(self, obj=None):
        """Method to delete an obj from a db

        Args:
            obj (string, optional): name of the obj. Defaults to None.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database
        """
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(factory)()

    def all_room_id(self, block_name):
        """Return the id of all the room in buildings"""
        result = self.__session.query(Building.room_id).filter(Building.block_name == block_name).order_by(Building.room_id).all()
        room_ids = [room_id[0] for room_id in result]
        return room_ids

    def close(self):
        """close session
        """
        self.__session.close()
