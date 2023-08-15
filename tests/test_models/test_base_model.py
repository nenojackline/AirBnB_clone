#!/usr/bin/python3
"""Unittest module for the BaseModel Class."""

from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from datetime import datetime
import json
import os
import re
import time
import unittest
import uuid


class TestBaseModel(unittest.TestCase):

    """Test Cases for the BaseModel class."""

    def setUp(self):
        """Sets up test methods."""
        pass

    def tearDown(self):
        """Tears down test methods."""
        self.resetStorage()
        pass

    def resetStorage(self):
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_3_instantiation(self):
        """Tests instantiation of BaseModel class."""

        fnb = BaseModel()
        self.assertEqual(str(type(fnb)), "<class 'models.base_model.BaseModel'>")
        self.assertIsInstance(fnb, BaseModel)
        self.assertTrue(issubclass(type(fnb), BaseModel))

    def test_3_init_no_args(self):
        """Tests __init__ with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as e:
            BaseModel.__init__()
        fnmsg = "__init__() missing 1 required positional argument: 'self'"
        self.assertEqual(str(e.exception), fnmsg)

    def test_3_init_many_args(self):
        """Tests __init__ with many arguments."""
        self.resetStorage()
        args = [i for i in range(1000)]
        fnb = BaseModel(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        fnb = BaseModel(*args)

    def test_3_attributes(self):
        """Tests attributes value for instance of a BaseModel class."""

        attributes = storage.attributes()["BaseModel"]
        fno = BaseModel()
        for fnk, fnv in attributes.items():
            self.assertTrue(hasattr(fno, fnk))
            self.assertEqual(type(getattr(fno, fnk, None)), fnv)

    def test_3_datetime_created(self):
        """Tests if updated_at & created_at are current at creation."""
        date_now = datetime.now()
        fnb = BaseModel()
        fndiff = fnb.updated_at - fnb.created_at
        self.assertTrue(abs(fndiff.total_seconds()) < 0.01)
        fndiff = fnb.created_at - date_now
        self.assertTrue(abs(fndiff.total_seconds()) < 0.1)

    def test_3_id(self):
        """Tests for unique user ids."""

        nl = [BaseModel().id for i in range(1000)]
        self.assertEqual(len(set(nl)), len(nl))

    def test_3_save(self):
        """Tests the public instance method save()."""

        fnb = BaseModel()
        time.sleep(0.5)
        date_now = datetime.now()
        fnb.save()
        fndiff = fnb.updated_at - date_now
        self.assertTrue(abs(fndiff.total_seconds()) < 0.01)

    def test_3_str(self):
        """Tests for __str__ method."""
        fnb = BaseModel()
        rex = re.compile(r"^\[(.*)\] \((.*)\) (.*)$")
        res = rex.match(str(fnb))
        self.assertIsNotNone(res)
        self.assertEqual(res.group(1), "BaseModel")
        self.assertEqual(res.group(2), fnb.id)
        fns = res.group(3)
        fns = re.sub(r"(datetime\.datetime\([^)]*\))", "'\\1'", fns)
        fnd = json.loads(fns.replace("'", '"'))
        fnd2 = fnb.__dict__.copy()
        fnd2["created_at"] = repr(fnd2["created_at"])
        fnd2["updated_at"] = repr(fnd2["updated_at"])
        self.assertEqual(fnd, fnd2)

    def test_3_to_dict(self):
        """Tests the public instance method to_dict()."""

        fnb = BaseModel()
        fnb.name = "Laura"
        fnb.age = 23
        fnd = fnb.to_dict()
        self.assertEqual(fnd["id"], fnb.id)
        self.assertEqual(fnd["__class__"], type(fnb).__name__)
        self.assertEqual(fnd["created_at"], fnb.created_at.isoformat())
        self.assertEqual(fnd["updated_at"], fnb.updated_at.isoformat())
        self.assertEqual(fnd["name"], fnb.name)
        self.assertEqual(fnd["age"], fnb.age)

    def test_3_to_dict_no_args(self):
        """Tests to_dict() with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as e:
            BaseModel.to_dict()
        fnmsg = "to_dict() missing 1 required positional argument: 'self'"
        self.assertEqual(str(e.exception), fnmsg)

    def test_3_to_dict_excess_args(self):
        """Tests to_dict() with too many arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as e:
            BaseModel.to_dict(self, 98)
        fnmsg = "to_dict() takes 1 positional argument but 2 were given"
        self.assertEqual(str(e.exception), fnmsg)

    def test_4_instantiation(self):
        """Tests instantiation with **kwargs."""

        my_model = BaseModel()
        my_model.name = "Holberton"
        my_model.my_number = 89
        my_model_json = my_model.to_dict()
        my_new_model = BaseModel(**my_model_json)
        self.assertEqual(my_new_model.to_dict(), my_model.to_dict())

    def test_4_instantiation_dict(self):
        """Tests instantiation with **kwargs from custom dict."""
        fnd = {"__class__": "BaseModel",
             "updated_at":
             datetime(2050, 12, 30, 23, 59, 59, 123456).isoformat(),
             "created_at": datetime.now().isoformat(),
             "id": uuid.uuid4(),
             "var": "foobar",
             "int": 108,
             "float": 3.14}
        fno = BaseModel(**fnd)
        self.assertEqual(fno.to_dict(), fnd)

    def test_5_save(self):
        """Tests that storage.save() is called from save()."""
        self.resetStorage()
        fnb = BaseModel()
        fnb.save()
        key = "{}.{}".format(type(fnb).__name__, fnb.id)
        fnd = {key: fnb.to_dict()}
        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))
        with open(FileStorage._FileStorage__file_path,
                  "r", encoding="utf-8") as fnf:
            self.assertEqual(len(fnf.read()), len(json.dumps(fnd)))
            fnf.seek(0)
            self.assertEqual(json.load(fnf), fnd)

    def test_5_save_no_args(self):
        """Tests save() with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as e:
            BaseModel.save()
        fnmsg = "save() missing 1 required positional argument: 'self'"
        self.assertEqual(str(e.exception), fnmsg)

    def test_5_save_excess_args(self):
        """Tests save() with too many arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as e:
            BaseModel.save(self, 98)
        fnmsg = "save() takes 1 positional argument but 2 were given"
        self.assertEqual(str(e.exception), fnmsg)


if __name__ == '__main__':
    unittest.main()
