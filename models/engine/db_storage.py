#!/usr/bin/python3
"""
DB storage module
"""

import os
import sys
import shlex
from os import getenv
from sqlalchemy import create_engine, distinct, update, func, select
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.building import Building
from models.user import User
from models.student import Student
from models.maintenance_request import Maintenance
from models.leave_request import Leave
from sqlalchemy.orm import aliased
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
#from models.facility import Facility
from sqlalchemy import and_, or_


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
                      "Maintenance": Maintenance
                      #"Facility": Facility
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

    def insert_student(self, name, ID, Country, room_id=None,
                       room_number=None):
        """Base a student base on his country
            * if all 5 arguments are given student should be insert manuelly in
                a specific room, considering room_id as Zone
                where to insert the student.
            * if only 4 arguments are provided insert a student randomly
        """
        student_name = name
        if "_" in name:
            student_name = name.replace('_', ' ')
        student_id = ID
        if "_" in ID:
            student_id = ID.replace('_', ' ')
        Student_country = Country
        if "_" in Country:
            Student_country = Country.replace('_', ' ')

        if room_id and not room_number:
            """insert a student randomly"""
            result = (self.__session.query(Student.Country, Student.Zone)
                      .filter(Student.Room_ID == room_id).all())
            zones = [result[i][1] for i in range(len(result))]
            countries = [result[j][0] for j in range(len(result))]

            if Student_country not in countries:
                count = 0
                for country in countries:
                    if country is None:
                        try:
                            self.__session.query(Student).filter(
                                Student.Room_ID == room_id,
                                Student.Zone == zones[count]
                            ).update({
                                Student.Student_name: student_name,
                                Student.Student_ID: student_id,
                                Student.Country: Student_country
                            }, synchronize_session='fetch')
                            self.save()

                            room_zone = (self.__session
                                         .query(
                                             Building.room_number,
                                             Student.Zone).join(
                                                Student,
                                                Building.room_id
                                                == Student.Room_ID)
                                         .filter(
                                             Student.Student_ID == student_id)
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
                    return 1

                self.__session.query(Student).filter(
                    Student.Room_ID == id_room[0],
                    Student.Zone == zone).update({
                        Student.Student_name: student_name,
                        Student.Student_ID: student_id,
                        Student.Country: Student_country
                        }, synchronize_session='fetch')

                self.save()

                return 2

            except Exception as e:
                print("The Student already exist in the Building")
                return 3

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
                        return -1

                obj = (
                    self.__session.query(Building)
                    .filter_by(room_id=obj_id[0])
                    .first()
                )

                self.delete(obj)
                self.save()
                print("Room {} deleted".format(obj_name))
                return 1
            except Exception:
                print("The room does not exist.")
                return 2

        elif obj_type == "block":
            
            room_existence = (self.__session.query(Building.block_name)
                              .filter(Building.block_name == obj_name)
                              .limit(1).first())
            if room_existence:
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
                    return 1
                else:
                    print("There are student in this building."
                          " move students first.")
                    return -1
            else:
                return -2

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
                            Country=None,
                            user_id=None
                            )
                            )

                self.__session.execute(stmt)
                self.save()
                return 1

            else:
                print("The Student does not exist.")
                return (-1)

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
                    return 1
                else:
                    print("There is a Student living at this zone.")
                    return -1
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
                                    .filter(Building.room_number
                                            .like(f"{block_name}-%"))
                                    )
                                    ).scalar())
                zone_count.append(count_result)
            return zone_count

    def get_application(self, app_type):
        """Get applicant name and time"""
        if app_type == "application":
            results = (
                self.__session.query(
                    Student.Student_name, Leave.created_at
                )
                .join(Leave, Student.Student_ID == Leave.student_id)
                .filter(Leave.status.is_(None))
                .limit(5)
                .all()
            )
            return results
        else:
            query = (
                self.__session.query(
                    Student.Student_name, Maintenance.created_at
                )
                .join(Maintenance,
                      Student.Student_ID == Maintenance.student_id)
                .filter(Maintenance.status.is_(None))
                .limit(5)
            )
            return query.all()

    def get_all_zones_residents(self, block_name):
        """Get all zones from a building"""
        query = self.__session.query(
            Building.room_number, Student.Student_name, Student.Student_ID,
            Student.Country, Student.Zone
        ).join(
            Student, Building.room_id == Student.Room_ID
        ).filter(
            Building.room_number.like(f"{block_name}-%")
        )

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
            all_zones = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
                         "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
                         "W", "X", "Y", "Z"]
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
                .filter(User.id == self.get_first_user()[0]).scalar())

    def get_all_rooms(self):
        """Get all rooms"""
        return self.__session.query(Building.room_number).all()

    def get_all_zones(self, room):
        """Get all zones of a room"""
        results = (
            self.__session.query(Student.Zone)
            .filter(Student.Room_ID.in_(
                self.__session.query(Building.room_id)
                .filter(Building.room_number == room)
                )).all())
        return results

    def get_user(self, username):
        """Get user by username"""
        return self.__session.query(User).filter_by(username=username).first()

    def get_user_object(self, id):
        """Retrieve user object"""
        return self.__session.query(User).filter_by(id=id).first()

    def get_first_user(self):
        """Get the id of the first user"""
        query = (self.__session.query(User.id)
                 .order_by(User.created_at).limit(1).first())
        return query

    def get_user_id_update_student(self, username, student_id):
        u = self.__session.query(User).filter_by(username=username).all()
        for user in u:
            if user.verify_password(password=student_id):
                self.__session.query(Student).filter(
                    Student.Student_ID == student_id
                    ).update({"user_id": user.id})
                self.save()

    def get_user_id_from_students(self, st_id):
        """Get the user id from student table"""
        query = (self.__session.query(Student.user_id)
                 .filter(Student.Student_ID == st_id).first())
        return query

    def delete_user(self, u_id):
        """Delete user from users table"""
        self.__session.query(User).filter(User.id == u_id).delete()
        self.save()

    def get_student_infos_before(self, st_id):
        """Get the infos of th student before movingg him"""
        query = (self.__session.query(Student.Student_name, Student.Country)
                 .filter(Student.Student_ID == st_id).all())
        return query

    def get_search_student(self, student_id):
        """Get student infos"""
        query = (
            self.__session.query(
                Building.hostel_id,
                Building.room_number,
                Student.Student_name,
                Student.Country,
                Student.Zone
                )
                .join(Student, Building.room_id == Student.Room_ID)
                .filter(Student.Student_ID == student_id)
                )
        return query.all()
    
    def get_all_room_residents(self, room_number):
        """Get all room residents"""
        result = self.__session.query(
            Building.hostel_id,
            Building.room_number,
            Student.Student_name,
            Student.Country,
            Student.Zone
        ).join(Student, Building.room_id == Student.Room_ID).filter(
            Building.room_number == room_number
        ).all()
        return result

    def get_leaves(self):
        """Get all leaves"""
        query = (
            self.__session.query(
                Student.Student_name, 
                Student.Student_ID, 
                Leave.start_date, 
                Leave.end_date, 
                Leave.description, 
                Leave.place
            )
            .join(Leave, Student.Student_ID == Leave.student_id)
            .filter(Leave.c_sa == None)
            .filter(Leave.c_school != None)
        )
        return query.all()

    def update_leave_approval(self, student_id, res_type):
        """Update c_sa column to 'yes' for a specific student leave"""
        self.__session.query(Leave).filter_by(student_id=student_id).update({"c_sa": res_type,
                                                                             "status": res_type})
        self.save()

    def get_on_leave_student(self):
        """Get all students who are on leave"""
        results = self.__session.query(
                Student.Student_name,
                Leave.student_id,
                Leave.end_date,
                Leave.place
            ).join(
                Leave, Student.Student_ID == Leave.student_id
            ).filter(
                Leave.status.isnot(None)
            ).all()
        return results

    def get_over_stay_students(self):
        """Get overstay students"""
        StudentAlias = aliased(Student)

        results = (
            self.__session.query(StudentAlias.Student_name,
                                 Leave.student_id,
                                 Leave.end_date,
                                 Leave.place)
            .join(Leave, StudentAlias.Student_ID == Leave.student_id)
            .filter(
                Leave.status.isnot(None),
                Leave.date_out.isnot(None),
                Leave.date_in < func.CURDATE()
            )
            .all()
        )
        return results

    def get_all_user_infos(self, user_id):
        """Get user informations"""
        query = self.__session.query(
            Building.room_number,
            Student.Student_name,
            Student.Student_ID,
            Student.Zone
        ).join(
            Student, Building.room_id == Student.Room_ID
        ).filter(
            Student.user_id == user_id
        )
        return query.all()

    def get_room_capacity(self, room_number):
        """Get number of resident in a room"""
        subquery = self.__session.query(Building.room_id).filter(Building.room_number == room_number).subquery()

        count_query = self.__session.query(func.count(Student.Zone)).filter(Student.Room_ID.in_(subquery))
        return count_query.scalar()

    def user_roommates(self, user_id):
        """Get all user roommmate"""
        subquery = (
            self.__session.query(Student.Room_ID)
            .filter(Student.user_id == user_id)
            .subquery()
        )


        results = (
            self.__session.query(Student.Student_name, Student.user_id)
            .filter(
                Student.Room_ID.in_(subquery),
                Student.user_id.isnot(None)
            )
            .all()
                )
        return results


    def get_leaves_object(self,student_id, start_date, end_date, place):
        """Get leave object"""
    
        query = self.__session.query(Leave.leave_id).filter(
            and_(
                Leave.student_id == student_id,
                Leave.start_date == start_date,
                Leave.end_date == end_date,
                Leave.place == place,
                Leave.status == None
            )
        )
        
        return query.all()
    

    def update_leave_school_response(self, leave_id, res_type):
        """update leave by school response"""
        self.__session.query(Leave).filter_by(leave_id=leave_id).update({"c_school": res_type})
        self.save()

    def check_leave_status(self, leave_id):
        """Check leave status before processing"""
        return self.__session.query(Leave.c_school).filter(Leave.leave_id == leave_id).scalar()

    def get_student_name_email_to_send_conf(self, student_id):
        """Get student infos"""
        subquery = self.__session.query(Student.user_id).filter(Student.Student_ID == student_id).subquery()

        results = self.__session.query(User.full_name, User.email).filter(User.id.in_(subquery)).all()
        return results