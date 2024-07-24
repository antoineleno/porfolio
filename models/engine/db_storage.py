#!/usr/bin/python3
"""
DB storage module
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.building import Building
from models.user import User
from models.student import Student
from models.facility import Facility


class DBStorage:
    """DBStorage
    Class to manage objects storage to DB
    """
    __engine = None
    __session = None

    def __init__(self):
        """Contructor method
        """
        db_user = os.getenv("MYUSER")
        db_password = os.getenv("MYPWD")
        host = os.getenv("MYHOST")
        db_name = os.getenv("MYDB")
        env = os.getenv("MYENV")

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
                      "Facility": Facility}
        obj_result = {}
        cls = cls if not isinstance(cls, str) else allclasses.get(cls)
        if cls is None:
            for cls in allclasses:
                objs = self.__session.query(cls).all()
                for obj in objs:
                    obj_result["{}.{}".format(obj.__name__, obj.id)] = obj
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                obj_result["{}.{}".format(obj.__name__, obj.id)] = obj
        return obj_result

    def new(self, obj):
        """new : to add an an obj to a session

        Args:
            obj (instance): Obj created to be addred
        """
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

    def close(self):
        """close session
        """
        self.__session.close()
