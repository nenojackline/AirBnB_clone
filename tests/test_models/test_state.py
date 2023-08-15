#!/usr/bin/python3
"""Unittest module for the State Class."""

import unittest
from datetime import datetime
import time
from models.state import State
import re
import json
from models.engine.file_storage import FileStorage
import os
from models import storage
from models.base_model import BaseModel


class TestState(unittest.TestCase):

    """Test Cases for the State class."""

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

    def test_8_instantiation(self):
        """Tests instantiation of State class."""

        fnb = State()
        self.assertEqual(str(type(fnb)), "<class 'models.state.State'>")
        self.assertIsInstance(fnb, State)
        self.assertTrue(issubclass(type(fnb), BaseModel))

    def test_8_attributes(self):
        """Tests the attributes of State class."""
        attributes = storage.attributes()["State"]
        fno = State()
        for fnk, fnv in attributes.items():
            self.assertTrue(hasattr(fno, fnk))
            self.assertEqual(type(getattr(fno, fnk, None)), fnv)


if __name__ == "__main__":
    unittest.main()
