#!/usr/bin/python3

from models.student import Student
from models.__init__ import storage

obj = Student()
obj.Student_name = "Amadou Bah"
obj.Student_ID = "AIU22102018"
obj.Country = "Guinea"
obj.Room_ID = "0262517a49"
obj.Zone = "A"

storage.new(obj)
storage.save()
