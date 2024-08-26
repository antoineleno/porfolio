#!/usr/bin/python3
"""
TEst hostel module
"""

import unittest
import uuid
from datetime import datetime
from models.leave_request import Leave
from models.base_model import BaseModel


class TestLeave(unittest.TestCase):
    """Class to test Leave class"""
    def test_Leave(self):
        """Test if Leave is a sub class of base_model"""
        self.assertTrue(issubclass(Leave, BaseModel))

    def test_leave_instance_and_attribute(self):
        """
        Test if leave can create an instance
        Test user class attribute
        """
        my_instance = Leave()
        self.assertIsInstance(my_instance, Leave)

    def test_kwargs(self):
        """
        Test if we can pass attribute to class
        """
        my_leave = Leave(place="KL")
        self.assertEqual(my_leave.place, "KL")

    def test_id_attriubte(self):
        """
        Test id attriubte
        """
        my_new_leave = Leave()
        uuid_obj = uuid.UUID(my_new_leave.id)
        self.assertTrue(uuid.UUID(my_new_leave.id, version=4))
        self.assertIsInstance(uuid_obj, uuid.UUID)

    def test_created_updated_at(self):
        """
        Test created at and updated at attributes
        """
        my_leave = Leave()
        current_date = datetime.now()
        my_leave.start_date = current_date
        my_leave.end_date = current_date
        my_leave.place = "KL"
        my_leave.c_school = "confirm"
        my_leave.status = "approved"
        my_leave.overstay = "yes"
        my_leave.date_out = current_date
        my_leave.date_in = current_date
        self.assertIsInstance(my_leave.created_at, datetime)
        self.assertIsInstance(my_leave.updated_at, datetime)
        self.assertIsInstance(my_leave.start_date, datetime)
        self.assertIsInstance(my_leave.end_date, datetime)
        self.assertIsInstance(my_leave.place, str)
        self.assertIsInstance(my_leave.c_school, str)
        self.assertIsInstance(my_leave.status, str)
        self.assertIsInstance(my_leave.overstay, str)
        self.assertIsInstance(my_leave.date_out, datetime)
        self.assertIsInstance(my_leave.date_in, datetime)

    def test_kwargs(self):
        """
        Test if we can pass attribute to class
        """
        my_leave = Leave(place="USA")
        self.assertEqual(my_leave.place, "USA")

    def test_id_attriubte(self):
        """
        Test id attriubte
        """
        my_new_leave = Leave()
        uuid_obj = uuid.UUID(my_new_leave.id)
        self.assertTrue(uuid.UUID(my_new_leave.id, version=4))
        self.assertIsInstance(uuid_obj, uuid.UUID)

    def test_str_representation(self):
        """
        Test string representation for User
        """
        my_A = Leave()
        ex_op = f"[{my_A.__class__.__name__}] ({my_A.id}) {my_A.__dict__}"
        self.assertEqual(str(my_A), ex_op)

    def test_str_rpr_with_attribute(self):
        """
        Test case where kwarg is provided
        """
        my_A = Leave(name="Antoine")
        ex_op = f"[{my_A.__class__.__name__}] ({my_A.id}) {my_A.__dict__}"
        self.assertEqual(str(my_A), ex_op)

    def test_str_rpr_with_attribute_not_kwarg(self):
        """
        Test str rpr case where attriube is assign
        not using kwarg
        """
        my_A = Leave()
        my_A.name = "Antoine"
        ex_op = f"[{my_A.__class__.__name__}] ({my_A.id}) {my_A.__dict__}"
        self.assertEqual(str(my_A), ex_op)

    def test_user_attribute_name(self):
        """
        Test user attributes type
        """
        my_A = Leave(description="For holiday", place="France")
        self.assertEqual(type(my_A.description), str)
        self.assertEqual(type(my_A.place), str)

    def test_str_representation_with_attributes(self):
        """
        Test user with attributes all type
        """
        my_A = Leave()
        my_A.my_list = [1, 2, 4]
        my_A.dict = {"A": 2, "B": 5, "C": 6}
        output = f"[{my_A.__class__.__name__}] ({my_A.id}) {my_A.__dict__}"
        self.assertEqual(str(my_A), output)

    def test_to_dict_with_attriube(self):
        """
        Test to dict method on user class
        with not attribute and with attributes
        """
        my_leave = Leave()
        my_leave.place = "Malaysia"
        my_leave.my_list = [1, 2, 4]
        my_leave.my_tuple = (1, 2, 4)
        my_leave.my_dict = {"A": 1, "B": 2, "C": 4}
        my_model_dict_repr = my_leave.to_dict()
        class_name = f"{my_leave.__class__.__name__}"
        dictionary = my_leave.__dict__
        expected_dict = {"__class__": class_name}
        expected_dict.update(dictionary)
        self.assertDictEqual(my_model_dict_repr, expected_dict)

    def test_save_method_without_storage(self):
        """Test save method without storage"""
        my_user = Leave()
        self.assertIsInstance(my_user.updated_at, datetime)

    def test_update_at_created_at_assignemt(self):
        """test update_at and created_at"""
        with self.assertRaises(ValueError):
            my_model = Leave(created_at="12pm", updated_at="12pm")
            self.assertEqual(my_model.created_at, "12pm")

    def test_attribute_error(self):
        """Test case where attribue does not exit"""
        with self.assertRaises(AttributeError):
            my_review = Leave()
            my_review.calculate()
