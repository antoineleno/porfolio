#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.building import Building
from models.hostel import Hostel
from models.student import Student
import shlex

class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''
    classes = {
               'BaseModel': BaseModel, 'User': User, 'Building': Building,
               'Hostel': Hostel, 'Student': Student
              }
   
    def do_create(self, args):
        """ Create an object of any class"""
        arguments = shlex.split(args)
        f_arguments = arguments[1:]
        print(f_arguments)
        
        if not args:
            print("** class name missing **")
            return
        elif arguments[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        new_instance = globals()[arguments[0]]()
        for my_args in f_arguments:
            key, value = my_args.split("=")
            setattr(new_instance, key, value)
        storage.new(new_instance)
        storage.save()
        print(new_instance.id)

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

if __name__ == "__main__":
    HBNBCommand().cmdloop()
