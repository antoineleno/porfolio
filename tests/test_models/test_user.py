#!/usr/bin/python3
"""
console module
    1 - Class to test Amenity
    2 - Class to test
"""

import unittest
import uuid
from datetime import datetime
from models.user import User
from models.base_model import BaseModel


class TestUser(unittest.TestCase):
    """Class to test user class"""
    def test_Usr(self):
        """Test if Usr is a sub class of base_model"""
        self.assertTrue(issubclass(User, BaseModel))

    def test_user_instance_and_attribute(self):
        """
        Test if user can create an instance
        Test user class attribute
        """
        my_instance = User()
        self.assertIsInstance(my_instance, User)
        my_instance.email = "lenomadeleineantoine@gmail.com"
        my_instance.password = "22@abantoine"
        my_instance.first_name = "Antoine"
        my_instance.last_name = "LENO"
        self.assertEqual(my_instance.password, "22@abantoine")
        self.assertEqual(my_instance.email, "lenomadeleineantoine@gmail.com")
        self.assertEqual(my_instance.first_name, "Antoine")
        self.assertEqual(my_instance.last_name, "LENO")

    def test_kwargs(self):
        """
        Test if we can pass attribute to class
        """
        my_Amenity = User(name="Antoine")
        self.assertEqual(my_Amenity.name, "Antoine")

    def test_id_attriubte(self):
        """
        Test id attriubte
        """
        my_new_user = User()
        uuid_obj = uuid.UUID(my_new_user.id)
        self.assertTrue(uuid.UUID(my_new_user.id, version=4))
        self.assertIsInstance(uuid_obj, uuid.UUID)

    def test_created_updated_at(self):
        """
        Test created at and updated at attributes
        """
        my_user = User()
        self.assertIsInstance(my_user.created_at, datetime)
        self.assertIsInstance(my_user.updated_at, datetime)

    def test_str_representation(self):
        """
        Test string representation for User
        """
        my_A = User()
        ex_op = f"[{my_A.__class__.__name__}] ({my_A.id}) {my_A.__dict__}"
        self.assertEqual(str(my_A), ex_op)

    def test_str_rpr_with_attribute(self):
        """
        Test case where kwarg is provided
        """
        my_A = User(name="Antoine")
        ex_op = f"[{my_A.__class__.__name__}] ({my_A.id}) {my_A.__dict__}"
        self.assertEqual(str(my_A), ex_op)

    def test_str_rpr_with_attribute_not_kwarg(self):
        """
        Test str rpr case where attriube is assign
        not using kwarg
        """
        my_A = User()
        my_A.name = "Antoine"
        ex_op = f"[{my_A.__class__.__name__}] ({my_A.id}) {my_A.__dict__}"
        self.assertEqual(str(my_A), ex_op)

    def test_user_attribute_name(self):
        """
        Test user attributes type
        """
        my_A = User(first_name="Antoine", last_name="LENO",
                    email="lenoantoine@gmail.com",
                    password="antoineleno")
        self.assertEqual(type(my_A.email), str)
        self.assertEqual(type(my_A.password), str)
        self.assertEqual(type(my_A.first_name), str)
        self.assertEqual(type(my_A.last_name), str)

    def test_str_representation_with_attributes(self):
        """
        Test user with attributes all type
        """
        my_A = User()
        my_A.my_list = [1, 2, 4]
        my_A.dict = {"A": 2, "B": 5, "C": 6}
        output = f"[{my_A.__class__.__name__}] ({my_A.id}) {my_A.__dict__}"
        self.assertEqual(str(my_A), output)

    def test_to_dict_with_attriube(self):
        """
        Test to dict method on user class
        with not attribute and with attributes
        """
        my_User = User()
        my_User.name = "Swimming Pool"
        my_User.my_list = [1, 2, 4]
        my_User.my_tuple = (1, 2, 4)
        my_User.my_dict = {"A": 1, "B": 2, "C": 4}
        my_model_dict_repr = my_User.to_dict()
        class_name = f"{my_User.__class__.__name__}"
        dictionary = my_User.__dict__
        expected_dict = {"__class__": class_name}
        expected_dict.update(dictionary)
        self.assertDictEqual(my_model_dict_repr, expected_dict)

    def test_save_method_without_storage(self):
        """Test save method without storage"""
        my_user = User()
        self.assertIsInstance(my_user.updated_at, datetime)

    def test_update_at_created_at_assignemt(self):
        """test update_at and created_at"""
        with self.assertRaises(ValueError):
            my_model = User(created_at="12pm", updated_at="12pm")
            self.assertEqual(my_model.created_at, "12pm")

    def test_attribute_error(self):
        """Test case where attribue does not exit"""
        with self.assertRaises(AttributeError):
            my_review = User()
            my_review.calculate()
