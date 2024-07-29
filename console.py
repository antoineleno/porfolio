#!/usr/bin/python3
"""
console module
"""

import cmd
import models
from models.base_model import BaseModel
from models.hostel import Hostel
from models.building import Building
from models.student import Student
from models.user import User
from models import storage


import os
import sys
import shlex

class CAMPUSCommand(cmd.Cmd):
    """Console class"""
    prompt = '(campus) ' if sys.__stdin__.isatty() else ''
    classes = {
               'BaseModel': BaseModel, 'User': User, 'Hostel': Hostel,
               'Building': Building, 'Student': Student
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
        * User: create User fist_name last_name email password
            example: create User Antoine LENO lenoantoine@gmail.com antoinepwd
        * Hostel: create Hostel hostel_type(Male/Female)
            example: create Hostel Male
        """

        arguments = shlex.split(args)
        people_count = arguments[-1]

        if arguments[0] == "Building":
            del arguments[-1]
            f_arguments = arguments[1:-2]
    
            name = arguments[2].split('=')[1]
    
            for i in range(1, int(arguments[-2]) + 1):
                arguments_copy = f_arguments[:]
                for j in range(1, int(arguments[-1]) + 1):
                    if j < 10:
                        arguments_copy.append("room_number={}-{}-0{}".format(name, i, j))
                    else:
                        arguments_copy.append("room_number={}-{}-{}".format(name, i, j))
                    print(arguments_copy[-1])
                    if not args:
                        print("** class name missing **")
                        return
                    elif arguments[0] not in CAMPUSCommand.classes:
                        print("** class doesn't exist **")
                        return
                    new_instance = globals()[arguments[0]]()
                    for my_args in arguments_copy:
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
                for l in range(int(people_count)):
                    new_argument = "Student Room_ID={} Zone={}".format(all_room_id[k], all_zones[l])
                    self.do_create(new_argument)
            
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
        


if __name__ == '__main__':
    CAMPUSCommand().cmdloop()