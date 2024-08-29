#!/usr/bin/python3
"""
console module
"""

import cmd
import models
from models.base_model import BaseModel
from models.hostel import Hostel
from models.building import Building
from models.leave_request import Leave
from models.student import Student
from models.user import User
from models.facility import Facility
from models import storage
from models.maintenance_request import Maintenance


import os
import sys
import shlex
import csv


class CAMPUSCommand(cmd.Cmd):
    """Console class"""
    prompt = '(campus) ' if sys.__stdin__.isatty() else ''
    classes = {
               'BaseModel': BaseModel, 'User': User, 'Hostel': Hostel,
               'Building': Building, 'Student': Student, 'Leave': Leave,
<<<<<<< HEAD
               'Maintenance': Maintenance
=======
               'Facility': Facility
>>>>>>> f7a7211ebb636cae434febacaa9df943dcc7ffba
              }

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """Called when an empty line is entered"""
        pass

    def do_EOF(self, line):
        """Handle End-of-File (EOF) condition to exit the program gracefully"""
        print()
        return True

    def do_create(self, args):
        """ Create an object of any type
        * Building: create Building hostel_id block_name number of level
                        number of room per level number of student/room.
                        hostel_id 1 for male and 2 for female
            example: create Building hostel_id=1 block_name="25E" 4 14 4
                To create building and student at the same time.
        * User: create User full_name user_name password role
            example: create User full_name=Antoine user_name=lenoantoine role=admin
                    email=lenoantoine@gmail.com password=antoinepw
        * Hostel: create Hostel hostel_type(Male/Female)
            example:  create Hostel hostel_type="Male"
        * if you try to insert a student and he already exists in the
        db and error message will be printed.
        * Apply for a leave
            example: create Leave student_id="AIU22102031"
            start_date="2024-08-16 09:00:00"
            end_date="2024-08-16 09:00:00"
            description="Visit" place="KK"

        """

        arguments = shlex.split(args)
        people_count = arguments[-1]

        if arguments[0] == "Building":
            del arguments[-1]
            f_arguments = arguments[1:-2]

            name = arguments[2].split('=')[1]
            block_names = []
            for i in range(1, 3):
                block_names += storage.all_block_name(i)

            if name in block_names:
                print("The block already exists please create another block.")
                return

            for i in range(1, int(arguments[-2]) + 1):
                arg_copy = f_arguments[:]
                for j in range(1, int(arguments[-1]) + 1):
                    if j < 10:
                        arg_copy.append("room_number={}-{}-0{}".format(
                            name, i, j))
                    else:
                        arg_copy.append("room_number={}-{}-{}".format(
                            name, i, j))
                    print(arg_copy[-1])
                    if not args:
                        print("** class name missing **")
                        return
                    elif arguments[0] not in CAMPUSCommand.classes:
                        print("** class doesn't exist **")
                        return
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
                        storage.save()
            all_room_id = storage.all_room_id(name)
            all_zones = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]

            for k in range(len(all_room_id)):
                for m in range(int(people_count)):
                    new_argument = "Student Room_ID={} Zone={}".format(
                        all_room_id[k], all_zones[m])
                    self.do_create(new_argument)
            
            Amenity = ["bed", "table", "lamp"]
            for item in Amenity:
                amenity = Facility(name=item)
                storage.new(amenity)
                storage.save()
                new_instance.facilities.append(amenity)
            storage.save()
        
        else:
            f_arguments = arguments[1:]

            if not args:
                print("** class name missing **")
                return
            elif arguments[0] not in CAMPUSCommand.classes:
                print("** class doesn't exist **")
                return
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
                storage.save()
            if arguments[0] != "Student":
                print(new_instance.id)

    def do_insert(self, args):
        """insert a student into the storage
            usage: insert type_of_hostel studentName,studentID, Country
                    to insert a student according to the rule of country
                    Not two students of the same country in the same room
            example: insert 1 Antoine AIU22102031 Guinea (for male hostel)
                     insert 2 Amadou AIU22102018  Liberia (for Female hostel)

            usae: insert  studentName, Student_ID, Country,Zone, Room_Number
            example: insert Antoine AIU22102032 Guinea A 25E-4-02

            usage: insert using csv file: insert path of the file
            the first row of the file should be: Type of hostel(1 or 2)
                                                 student name
                                                 student ID
                                                 Country
                                                 as header
            example: insert student.csv
        """

        arguments = shlex.split(args)
        if len(arguments) == 4:
            Hostels = []
            Room_ID = []
            n = 1 if arguments[0] == "1" else 2
            Hostels = storage.all_block_name(n)
            for i in range(len(Hostels)):
                Room_ID += storage.all_room_id(Hostels[i])
                for i in range(len(Room_ID)):
                    answer = storage.insert_student(arguments[1],
                                                    arguments[2],
                                                    arguments[3].title(),
                                                    Room_ID[i])
                    if isinstance(answer, list):
                        print("Room: {} / Zone: {}".format(
                            answer[0][0], answer[0][1]))
                        return
                    elif answer == 404:
                        print("The student {} already exists in the hostel"
                              .format(arguments[2]))
                        return
            print("No place found for {} Insert him manuelly "
                  "or open a new building for him!".format(arguments[2]))

        elif len(arguments) == 5:
            rom_number, zone = storage.insert_student(arguments[0],
                                                      arguments[1],
                                                      arguments[2],
                                                      arguments[3].upper(),
                                                      arguments[4])
            print("Room: {} / Zone: {}".format(rom_number, zone))

        elif len(arguments) == 1:
            all_students = []
            try:
                with open("{}".format(arguments[0]), mode="r") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        all_students.append(row)
                del all_students[0]
            except FileNotFoundError:
                print("No file found.")

            for i in range(len(all_students)):
                new_argument = (all_students[i][0] +
                                " " + all_students[i][1] +
                                " " + all_students[i][2] +
                                " " + all_students[i][3])
                self.do_insert(new_argument)

        else:
            print("Incorrect syntax.")

    def do_delete(self, args):
        """_deleter : method to delete a building, room, zone, student

        Args:
            args (string): argument provided

        usage: delete room room_number (For room)
        example: delete room 24E-04-02

        usage: delete zone room_number
        example: delete zone {A/B/C/D} 24E-04-02
                 delete zone A 24E-04-05
        usage: delete student.csv
               delete student ID
        example: delete student AIU22102031
        example: delte student.csv
        """

        arguments = shlex.split(args)

        if len(arguments) >= 2:
            try:
                if arguments[0] == "block":
                    storage.object_to_delete(arguments[0], arguments[1])
                elif arguments[0] == "room":
                    storage.object_to_delete(arguments[0], arguments[1])
                elif arguments[0] == "zone":
                    storage.object_to_delete(arguments[0],
                                             arguments[1],
                                             arguments[2].upper())
                elif arguments[0] == "student":
                    storage.object_to_delete(arguments[0], arguments[1])
                else:
                    print("Incorrect syntax.")
            except Exception as e:
                print("Syntax error.")

        else:
            all_students = []
            try:
                with open("{}".format(arguments[0]), mode="r") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        all_students.append(row)
                del all_students[0]
            except FileNotFoundError:
                print("No file found.")
            for i in range(len(all_students)):
                new_argument = "student " + all_students[i][0]
                self.do_delete(new_argument)

            

if __name__ == '__main__':
    CAMPUSCommand().cmdloop()
