#!/usr/bin/python3
"""
test_building : to test building module
"""

import unittest
import uuid
from datetime import datetime
from models.building import Building
from models.base_model import BaseModel


class TestBuilding(unittest.TestCase):
    """Class to test building class"""
    def test_Building(self):
        """Test if building is a sub class of base_model"""
        self.assertTrue(issubclass(Building, BaseModel))

    def test_building_instance_and_attribute(self):
        """Test if building can create an instance
            Test building class attribute
        """
        my_instance = Building()
        self.assertIsInstance(my_instance, Building)
        my_instance.hostel_id = 1
        my_instance.block_name = "25E"
        my_instance.room_number = "25E-04-02"
        self.assertEqual(my_instance.hostel_id, 1)
        self.assertEqual(my_instance.block_name, "25E")
        self.assertEqual(my_instance.room_number, "25E-04-02")

    def test_kwargs(self):
        """Test if we can pass attribute to class"""
        my_building = Building(block_name="25E")
        self.assertEqual(my_building.block_name, "25E")
        my_new_building = Building(block_name="25E",
                                   hostel_id=1, room_number="25E-04-2")
        self.assertEqual(my_new_building.block_name, "25E")

    def test_id_attribute(self):
        """Test id attribute"""
        my_new_building = Building()
        uuid_obj = uuid.UUID(my_new_building.id)
        self.assertTrue(uuid.UUID(my_new_building.id, version=4))
        self.assertIsInstance(uuid_obj, uuid.UUID)

    def test_created_updated_at(self):
        """
        Test created at and updated at attributes
        """
        my_building = Building()
        self.assertIsInstance(my_building.created_at, datetime)
        self.assertIsInstance(my_building.updated_at, datetime)

    def test_str_representation(self):
        """
        Test string representation for building
        """
        my_A = Building()
        ex_op = f"[{my_A.__class__.__name__}] ({my_A.id}) {my_A.__dict__}"
        self.assertEqual(str(my_A), ex_op)

    def test_str_rpr_with_attribute(self):
        """
        Test case where kwarg is provided
        """
        my_A = Building(name="25E")
        ex_op = f"[{my_A.__class__.__name__}] ({my_A.id}) {my_A.__dict__}"
        self.assertEqual(str(my_A), ex_op)

    def test_str_rpr_with_attribute_not_kwarg(self):
        """
        Test str rpr case where attriube is assign
        not using kwarg
        """
        my_A = Building()
        my_A.block_name = "25D"
        ex_op = f"[{my_A.__class__.__name__}] ({my_A.id}) {my_A.__dict__}"
        self.assertEqual(str(my_A), ex_op)

    def test_building_attribute_name(self):
        """
        Test user attributes type
        """
        my_A = Building(block_name="25E", hostel_id=1,
                        room_number="25E-04-1")
        self.assertEqual(type(my_A.block_name), str)
        self.assertEqual(type(my_A.hostel_id), int)
        self.assertEqual(type(my_A.room_number), str)

    def test_str_representation_with_attributes(self):
        """
        Test Building with attributes all type
        """
        my_A = Building()
        my_A.my_list = [1, 2, 4]
        my_A.dict = {"A": 2, "B": 5, "C": 6}
        output = f"[{my_A.__class__.__name__}] ({my_A.id}) {my_A.__dict__}"
        self.assertEqual(str(my_A), output)

    def test_to_dict_with_attriube(self):
        """
        Test to dict method on user class
        with not attribute and with attributes
        """
        my_Buildin = Building()
        my_Buildin.block_name = "25E"
        my_Buildin.my_list = [1, 2, 4]
        my_Buildin.my_tuple = (1, 2, 4)
        my_Buildin.my_dict = {"A": 1, "B": 2, "C": 4}
        my_model_dict_repr = my_Buildin.to_dict()
        class_name = f"{my_Buildin.__class__.__name__}"
        dictionary = my_Buildin.__dict__
        expected_dict = {"__class__": class_name}
        expected_dict.update(dictionary)
        self.assertDictEqual(my_model_dict_repr, expected_dict)

    def test_save_datetime_objects(self):
        """Test save method without storage"""
        my_building = Building()
        self.assertIsInstance(my_building.updated_at, datetime)
        self.assertIsInstance(my_building.created_at, datetime)

    def test_update_at_created_at_assignemt(self):
        """test update_at and created_at"""
        with self.assertRaises(ValueError):
            my_model = Building(created_at="12pm", updated_at="12pm")
            self.assertEqual(my_model.created_at, "12pm")

    def test_attribute_error(self):
        """Test case where attribue does not exit"""
        with self.assertRaises(AttributeError):
            my_review = Building()
            my_review.calculate()
