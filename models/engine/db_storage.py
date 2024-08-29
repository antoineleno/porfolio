#!/usr/bin/python3
"""
DB storage module
"""

import os
import sys
import shlex
from os import getenv
from sqlalchemy import create_engine, distinct, update, func
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.building import Building
from models.user import User
from models.student import Student
from models.maintenance_request import Maintenance
from models.leave_request import Leave
<<<<<<< HEAD
from datetime import datetime, timedelta

=======
from models.facility import Facility
>>>>>>> f7a7211ebb636cae434febacaa9df943dcc7ffba

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
<<<<<<< HEAD
                      "Maintenance": Maintenance
=======
                      "Facility": Facility
>>>>>>> f7a7211ebb636cae434febacaa9df943dcc7ffba
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

    def all_room_id(self, b_name):
        """Return the id of all the rooms in buildings"""
        block_name = ""
        if "_" in b_name:
            block_name = b_name.replace("_", " ")
        else:
            block_name = b_name
            
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
        return [name[0] for name in result]

    def insert_student(self, f_name, f_ID, f_Country, room_id=None,
                       room_number=None):
        """Base a student base on his country
            * if all 5 arguments are given student should be insert manuelly in
                a specific room, considering room_id as Zone
                where to insert the student.
            * if only 4 arguments are provided insert a student randomly
        """

        if room_id and not room_number:
            """insert a student randomly"""
            name = ""
            Country = ""
            ID = ""
            if "_" in f_name:
                name = f_name.replace("_", " ")
            else:
                name = f_name
            if "_" in f_ID:
                ID = f_ID.replace("_", " ")
            else:
                ID = f_ID
            if "_" in f_Country:
                Country = f_Country.replace("_", " ")
            else:
                Country = f_Country
            

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

    def count_block(self, hostel_type):
        """Count number of blocks"""
        count = (self.__session
                 .query(func.count(func.distinct(Building.block_name)))
                 .filter(Building.hostel_id == hostel_type).scalar())
        return count

    def count_students(self, hostel_type, block_type=None):
        """Count number of students in a hostel or block."""
        if block_type:
            blocks_names = self.all_block_name(hostel_type)
            if len(blocks_names) != 0:
                student_count = []
                for block_name in blocks_names:
                    count = (self.__session
                             .query(func.count(Student.Student_ID))
                             .join(Building,
                                   Student.Room_ID == Building.room_id)
                             .filter(
                                 Building.room_number.like(f"{block_name}%"),
                                 Student.Student_ID.isnot(None)
                             ).scalar())
                    student_count.append(count)
                return student_count
        else:
            subquery = (self.__session
                        .query(Building.room_id)
                        .filter(Building.hostel_id == hostel_type).subquery())
            count = self.__session.query(func.count()).filter(
                Student.Room_ID.in_(subquery),
                Student.Student_ID.isnot(None)
                ).scalar()
            return count

    def count_zones(self, hostel_type):
        """Count number of zones in a block."""
        blocks_names = self.all_block_name(hostel_type)
        if len(blocks_names) != 0:
            zone_count = []
            for block_name in blocks_names:
                count_result = (self.__session
                                .query(func.count(Student.Zone))
                                .filter(Student.Room_ID.in_(
                                    self.__session.query(Building.room_id)
                                    .filter(Building.room_number.like(f"{block_name}-%"))
                                    )
                                    ).scalar())
                zone_count.append(count_result)
            return zone_count

    def get_application(self, app_type):
        """Get applicant name and time"""
        if app_type == "application":
            results = (self.__session.query(Student.Student_name, Leave.created_at)
                       .join(Leave, Student.Student_ID == Leave.student_id)
                       .filter(Leave.status == None)
                       .limit(5).all())
            return results
        else:
            query = (self.__session
                     .query(Student.Student_name,
                            Maintenance.created_at)
                            .join(Maintenance, Student.Student_ID == Maintenance.student_id)
                            .filter(Maintenance.status == None)
                            .limit(5))
            return query.all()


    def get_all_zones_residents(self, block_name):
        """Get all zones from a building"""
        query = (
            self.__session.query(Building.room_number,
                                 Student.Student_name,
                                 Student.Student_ID,
                                 Student.Country, Student.Zone)
                                 .join(Student, Building.room_id == Student.Room_ID)
                                 .filter(Building.room_number.like(f"{block_name}-%")))
        results = query.all()
        return results
    
    def time_since(self, message_time_str):
        """Parse the string into a datetime object"""
        message_time = datetime.strptime(message_time_str, '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        time_diff = now - message_time
        seconds = time_diff.total_seconds()
        minutes = seconds // 60
        hours = minutes // 60
        days = hours // 24

        if seconds < 60:
            return f"{int(seconds)} seconds ago"
        elif minutes < 60:
            return f"{int(minutes)} minutes ago"
        elif hours < 24:
            return f"{int(hours)} hours ago"
        else:
            return f"{int(days)} days ago"

    def create_a_new_object(self, args):
        arguments = shlex.split(args)
        people_count = arguments[-1]

        if arguments[0] == "Building":
            del arguments[-1]
            f_arguments = arguments[1:-2]

            name = arguments[2].split('=')[1]

            for i in range(1, int(arguments[-2]) + 1):
                arg_copy = f_arguments[:]
                for j in range(1, int(arguments[-1]) + 1):
                    if j < 10:
                        arg_copy.append("room_number={}-{}-0{}".format(
                            name, i, j))
                    else:
                        arg_copy.append("room_number={}-{}-{}".format(
                            name, i, j))

                    new_instance = globals()[arguments[0]]()
                    for my_args in arg_copy:
                        key, value = my_args.split("=")
                        if '_' in value:
                            new_value = value.replace('_', ' ')
                            setattr(new_instance, key, new_value)
                        else:
                            setattr(new_instance, key, value)

                    if os.getenv("CAMPUS_TYPE_STORAGE") == "db":
                        new_instance.save()
                    else:
                        self.save()
            
            all_room_id = self.all_room_id(name)
            all_zones = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
            for k in range(len(all_room_id)):
                for m in range(int(people_count)):
                    new_argument = "Student Room_ID={} Zone={}".format(
                        all_room_id[k], all_zones[m])
                    self.create_a_new_object(new_argument)
        else:
            f_arguments = arguments[1:]
            new_instance = globals()[arguments[0]]()
            for my_args in f_arguments:
                key, value = my_args.split("=")
                if '_' in value:
                    new_value = value.replace('_', ' ')
                    setattr(new_instance, key, new_value)
                else:
                    setattr(new_instance, key, value)
            if os.getenv("CAMPUS_TYPE_STORAGE") == "db":
                new_instance.save()
            else:
                self.save()
    
    def get_admin_name(self):
        """Get the name of the Admin"""
        return (self.__session
                .query(User.full_name)
                .filter(User.role == "admin").scalar())