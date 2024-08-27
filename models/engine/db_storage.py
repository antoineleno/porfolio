#!/usr/bin/python3
"""
DB storage module
"""

from os import getenv
from sqlalchemy import create_engine, distinct, update
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.building import Building
from models.user import User
from models.student import Student
from models.leave_request import Leave
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
        db_user = getenv("CAMPUS_MYSQL_USER")
        db_password = getenv("CAMPUS_MYSQL_PWD")
        db_name = getenv("CAMPUS_MYSQL_DB")
        host = getenv("CAMPUS_MYSQL_HOST")
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
                      "Leave": Leave,
                      "Facility": Facility
                      }
        obj_result = {}
        cls = cls if not isinstance(cls, str) else allclasses.get(cls)
        if cls is None:
            for cls in allclasses.values():
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
            existing_count = self.__session.query(Student).
            filter(Building.room_id == Student.Room_ID).count()
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

    def close(self):
        """close session
        """
        self.__session.close()

    def all_room_id(self, block_name):
        """Return the id of all the rooms in buildings"""
        result = (
            self.__session.query(Building.room_id)
            .filter(Building.block_name == block_name)
            .order_by(Building.room_id)
            .all())
        room_ids = [room_id[0] for room_id in result]

        return room_ids

    def all_block_name(self, hostel_type):
        """Return the name of all the blocks in the hostels"""
        result = (
            self.__session.query(distinct(Building.block_name))
            .filter(Building.hostel_id == hostel_type)
            .all())

        return [hostel_name[0] for hostel_name in result]

    def insert_student(self, name, ID, Country, room_id=None,
                       room_number=None):
        """Base a student base on his country
            * if all 5 arguments are given student should be insert manuelly in
                a specific room, considering room_id as Zone
                where to insert the student.
            * if only 4 arguments are provided insert a student randomly
        """

        if room_id and not room_number:
            """insert a student randomly"""
            result = (self.__session.query(Student.Country, Student.Zone)
                      .filter(Student.Room_ID == room_id).all())
            zones = [result[i][1] for i in range(len(result))]
            countries = [result[j][0] for j in range(len(result))]

            if Country not in countries:
                count = 0
                for country in countries:
                    if country is None:
                        try:
                            self.__session.query(Student).filter(
                                Student.Room_ID == room_id,
                                Student.Zone == zones[count]
                            ).update({
                                Student.Student_name: name,
                                Student.Student_ID: ID,
                                Student.Country: Country
                            }, synchronize_session='fetch')
                            self.save()

                            room_zone = (self.__session
                                         .query(
                                             Building.room_number,
                                             Student.Zone).join(
                                                Student,
                                                Building.room_id
                                                == Student.Room_ID)
                                         .filter(Student.Student_ID == ID)
                                         .all())

                            return (room_zone)

                        except Exception:
                            return (404)
                    count += 1
            else:
                return (0)
        else:
            try:
                zone = room_id
                id_room = (self.__session.query(Building.room_id)
                           .filter(Building.room_number == room_number)
                           .first())

                student_checking = (self.__session
                                    .query(Student.Student_ID)
                                    .join(Building,
                                          Building.room_id == Student.Room_ID)
                                    .filter(
                                        Building.room_id == id_room[0],
                                        Student.Zone == zone
                                        ).order_by(Student.Room_ID).all())

                if student_checking[0][0] is not None:
                    print("A student already exist in this Zone.")
                    return (room_number, zone)

                self.__session.query(Student).filter(
                    Student.Room_ID == id_room[0],
                    Student.Zone == zone).update({
                        Student.Student_name: name,
                        Student.Student_ID: ID,
                        Student.Country: Country
                        }, synchronize_session='fetch')

                self.save()

                return (room_number, zone)

            except Exception as e:
                print("The Student already exist in the Building")
                return (room_number, zone)

    def object_to_delete(self, obj_type, obj_name, zone=None):
        obj_id = ""
        if obj_type == "room":
            try:
                obj_id = (
                    self.__session.query(Building.room_id)
                    .filter_by(room_number=obj_name)
                    .first())

                checking_students = (
                    self.__session.query(Student.Student_ID)
                    .filter_by(Room_ID=obj_id[0])
                    .all())

                for i in range(len(checking_students)):
                    if checking_students[i][0] is not None:
                        print("There is a student in this room."
                              " Can't remove it")
                        return

                obj = (
                    self.__session.query(Building)
                    .filter_by(room_id=obj_id[0])
                    .first()
                )

                self.delete(obj)
                self.save()
                print("Room {} deleted".format(obj_name))
            except Exception:
                print("The room does not exist.")

        elif obj_type == "block":
            checking_block = (
                self.__session.query(Student.Student_ID)
                .join(Building, Building.room_id == Student.Room_ID)
                .filter(
                    Building.block_name == obj_name,
                    Student.Student_ID.isnot(None)
                    ).all())

            if (len(checking_block) == 0):
                self.__session.query(Building).filter_by(
                    block_name=obj_name
                    ).delete(
                        synchronize_session='fetch')
                self.save()
                print("Block {} deleted.".format(obj_name))
            else:
                print("There are student in this building."
                      " move students first.")

        elif obj_type == "student":

            room_id = (
                self.__session.query(Student.Room_ID)
                .filter(Student.Student_ID == obj_name)
                .scalar()
                )

            if room_id is not None:

                stmt = (
                    update(Student)
                    .where(
                        (Student.Room_ID == room_id) &
                        (Student.Student_ID == obj_name)
                        ).values(
                            Student_name=None,
                            Student_ID=None,
                            Country=None
                            )
                            )

                self.__session.execute(stmt)
                self.save()

            else:
                print("The Student does not exist.")

        else:
            room_id = (
                self.__session.query(Building.room_id)
                .filter(Building.room_number == zone)
                .scalar()
                )

            if room_id is not None:
                result = (
                    self.__session.query(Student.Student_ID)
                    .filter_by(Room_ID=room_id, Zone=obj_name)
                    .scalar())
                if result is None:
                    deleted_count = (
                        self.__session.query(Student)
                        .filter_by(Room_ID=room_id, Zone=obj_name)
                        .delete(synchronize_session='fetch'))
                    self.save()
                    print("Zone {} deleted".format(obj_name))
                else:
                    print("There is a Student living at this zone.")
            else:
                print("Zone does not exist.")
    def report(self, hostel_type):
        block_names = self.all_block_name(hostel_type)
        my_response = {}
        for name in block_names:    
            query = self.__session.query(
            Building.room_number,
            Student.Student_name,
            Student.Student_ID,
            Student.Country,
            Student.Zone
            ).join(
            Student,
            Building.room_id == Student.Room_ID
            ).filter(
            Student.Student_ID.isnot(None),
            Building.block_name == name
            )
            
            if len(query.all()) != 0:
                my_response[name] = query.all()

        
        return my_response