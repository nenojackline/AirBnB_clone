#!/usr/bin/python3
"""Module for TestHBNBCommand class."""

from console import HBNBCommand
from models.engine.file_storage import FileStorage
import unittest
import datetime
from unittest.mock import patch
import sys
from io import StringIO
import re
import os


class TestHBNBCommand(unittest.TestCase):

    """Tests HBNBCommand console."""

    attribute_values = {
        str: "foobar108",
        int: 1008,
        float: 1.08
    }

    reset_values = {
        str: "",
        int: 0,
        float: 0.0
    }

    test_random_attributes = {
        "strfoo": "barfoo",
        "intfoo": 248,
        "floatfoo": 9.8
    }

    def setUp(self):
        """Sets up test cases."""
        if os.path.isfile("file.json"):
            os.remove("file.json")
        self.resetStorage()

    def resetStorage(self):
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_help(self):
        """Tests the help command."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("help")
        fns = """
Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

"""
        self.assertEqual(fns, fnf.getvalue())

    def test_help_EOF(self):
        """Tests the help command."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("help EOF")
        fns = 'Handles End Of File character.\n        \n'
        self.assertEqual(fns, fnf.getvalue())

    def test_help_quit(self):
        """Tests the help command."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("help quit")
        fns = 'Exits the program.\n        \n'
        self.assertEqual(fns, fnf.getvalue())

    def test_help_create(self):
        """Tests the help command."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("help create")
        fns = 'Creates an instance.\n        \n'
        self.assertEqual(fns, fnf.getvalue())

    def test_help_show(self):
        """Tests the help command."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("help show")
        fns = 'Prints the string representation of an instance.\n        \n'
        self.assertEqual(fns, fnf.getvalue())

    def test_help_destroy(self):
        """Tests the help command."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("help destroy")
        fns = 'Deletes an instance based on the class name and id.\n        \n'
        self.assertEqual(fns, fnf.getvalue())

    def test_help_all(self):
        """Tests the help command."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("help all")
        fns = 'Prints all string representation of all instances.\n        \n'
        self.assertEqual(fns, fnf.getvalue())

    def test_help_count(self):
        """Tests the help command."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("help count")
        fns = 'Counts the instances of a class.\n        \n'
        self.assertEqual(fns, fnf.getvalue())

    def test_help_update(self):
        """Tests the help command."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("help update")
        fns = 'Updates an instance by adding or updating attribute.\n        \n'
        self.assertEqual(fns, fnf.getvalue())

    def test_do_quit(self):
        """Tests quit commmand."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("quit")
        fnmsg = fnf.getvalue()
        self.assertTrue(len(fnmsg) == 0)
        self.assertEqual("", fnmsg)
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("quit garbage")
        fnmsg = fnf.getvalue()
        self.assertTrue(len(fnmsg) == 0)
        self.assertEqual("", fnmsg)

    def test_do_EOF(self):
        """Tests EOF commmand."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("EOF")
        fnmsg = fnf.getvalue()
        self.assertTrue(len(fnmsg) == 1)
        self.assertEqual("\n", fnmsg)
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("EOF garbage")
        fnmsg = fnf.getvalue()
        self.assertTrue(len(fnmsg) == 1)
        self.assertEqual("\n", fnmsg)

    def test_emptyline(self):
        """Tests emptyline functionality."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("\n")
        fns = ""
        self.assertEqual(fns, fnf.getvalue())

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("                  \n")
        fns = ""
        self.assertEqual(fns, fnf.getvalue())

    def test_do_create(self):
        """Tests create for all classes."""
        for classname in self.classes():
            self.help_test_do_create(classname)

    def help_test_do_create(self, classname):
        """Helper method to test the create commmand."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = fnf.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)
        key = "{}.{}".format(classname, uid)
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("all {}".format(classname))
        self.assertTrue(uid in fnf.getvalue())

    def test_do_create_error(self):
        """Tests create command with errors."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("create")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("create garbage")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** class doesn't exist **")

    def test_do_show(self):
        """Tests show for all classes."""
        for classname in self.classes():
            self.help_test_do_show(classname)
            self.help_test_show_advanced(classname)

    def help_test_do_show(self, classname):
        """Helps test the show command."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = fnf.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("show {} {}".format(classname, uid))
        fns = fnf.getvalue()[:-1]
        self.assertTrue(uid in fns)

    def test_do_show_error(self):
        """Tests show command with errors."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("show")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("show garbage")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("show BaseModel")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("show BaseModel 6524359")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** no instance found **")

    def help_test_show_advanced(self, classname):
        """Helps test .show() command."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = fnf.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        fns = fnf.getvalue()
        self.assertTrue(uid in fns)

    def test_do_show_error_advanced(self):
        """Tests show() command with errors."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd(".show()")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("garbage.show()")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("BaseModel.show()")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd('BaseModel.show("6524359")')
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** no instance found **")

    def test_do_destroy(self):
        """Tests destroy for all classes."""
        for classname in self.classes():
            self.help_test_do_destroy(classname)
            self.help_test_destroy_advanced(classname)

    def help_test_do_destroy(self, classname):
        """Helps test the destroy command."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = fnf.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("destroy {} {}".format(classname, uid))
        fns = fnf.getvalue()[:-1]
        self.assertTrue(len(fns) == 0)

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd(".all()")
        self.assertFalse(uid in fnf.getvalue())

    def test_do_destroy_error(self):
        """Tests destroy command with errors."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("destroy")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("destroy garbage")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("destroy BaseModel")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("destroy BaseModel 6524359")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** no instance found **")

    def help_test_destroy_advanced(self, classname):
        """Helps test the destroy command."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = fnf.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd('{}.destroy("{}")'.format(classname, uid))
        fns = fnf.getvalue()[:-1]
        self.assertTrue(len(fns) == 0)

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd(".all()")
        self.assertFalse(uid in fnf.getvalue())

    def test_do_destroy_error_advanced(self):
        """Tests destroy() command with errors."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd(".destroy()")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("garbage.destroy()")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("BaseModel.destroy()")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd('BaseModel.destroy("6524359")')
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** no instance found **")

    def test_do_all(self):
        """Tests all for all classes."""
        for classname in self.classes():
            self.help_test_do_all(classname)
            self.help_test_all_advanced(classname)

    def help_test_do_all(self, classname):
        """Helps test the all command."""
        uid = self.create_class(classname)
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("all")
        fns = fnf.getvalue()[:-1]
        self.assertTrue(len(fns) > 0)
        self.assertIn(uid, fns)

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("all {}".format(classname))
        fns = fnf.getvalue()[:-1]
        self.assertTrue(len(fns) > 0)
        self.assertIn(uid, fns)

    def test_do_all_error(self):
        """Tests all command with errors."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("all garbage")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** class doesn't exist **")

    def help_test_all_advanced(self, classname):
        """Helps test the .all() command."""
        uid = self.create_class(classname)
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("{}.all()".format(classname))
        fns = fnf.getvalue()[:-1]
        self.assertTrue(len(fns) > 0)
        self.assertIn(uid, fns)

    def test_do_all_error_advanced(self):
        """Tests all() command with errors."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("garbage.all()")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** class doesn't exist **")

    def test_count_all(self):
        """Tests count for all classes."""
        for classname in self.classes():
            self.help_test_count_advanced(classname)

    def help_test_count_advanced(self, classname):
        """Helps test .count() command."""
        for i in range(20):
            uid = self.create_class(classname)
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("{}.count()".format(classname))
        fns = fnf.getvalue()[:-1]
        self.assertTrue(len(fns) > 0)
        self.assertEqual(fns, "20")

    def test_do_count_error(self):
        """Tests .count() command with errors."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("garbage.count()")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** class doesn't exist **")
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd(".count()")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** class name missing **")

    def test_update_1(self):
        """Tests update 1..."""
        classname = "BaseModel"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, attr, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd(cmd)
        fns = fnf.getvalue()
        self.assertEqual(len(fns), 0)
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        fns = fnf.getvalue()
        self.assertIn(attr, fns)
        self.assertIn(val, fns)

    def test_update_2(self):
        """Tests update 1..."""
        classname = "User"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, attr, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd(cmd)
        fns = fnf.getvalue()
        self.assertEqual(len(fns), 0)
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        fns = fnf.getvalue()
        self.assertIn(attr, fns)
        self.assertIn(val, fns)

    def test_update_3(self):
        """Tests update 1..."""
        classname = "City"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, attr, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd(cmd)
        fns = fnf.getvalue()
        self.assertEqual(len(fns), 0)
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        fns = fnf.getvalue()
        self.assertIn(attr, fns)
        self.assertIn(val, fns)

    def test_update_4(self):
        """Tests update 1..."""
        classname = "State"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, attr, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd(cmd)
        fns = fnf.getvalue()
        self.assertEqual(len(fns), 0)
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        fns = fnf.getvalue()
        self.assertIn(attr, fns)
        self.assertIn(val, fns)

    def test_update_5(self):
        """Tests update 1..."""
        classname = "Amenity"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, attr, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd(cmd)
        fns = fnf.getvalue()
        self.assertEqual(len(fns), 0)
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        fns = fnf.getvalue()
        self.assertIn(attr, fns)
        self.assertIn(val, fns)

    def test_update_6(self):
        """Tests update 1..."""
        classname = "Review"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, attr, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd(cmd)
        fns = fnf.getvalue()
        self.assertEqual(len(fns), 0)
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        fns = fnf.getvalue()
        self.assertIn(attr, fns)
        self.assertIn(val, fns)

    def test_update_7(self):
        """Tests update 1..."""
        classname = "Place"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, attr, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd(cmd)
        fns = fnf.getvalue()
        self.assertEqual(len(fns), 0)
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        fns = fnf.getvalue()
        self.assertIn(attr, fns)
        self.assertIn(val, fns)

    def test_update_everything(self):
        """Tests update command with errthang, like a baws."""
        for classname, cls in self.classes().items():
            uid = self.create_class(classname)
            for attr, value in self.test_random_attributes.items():
                if type(value) is not str:
                    pass
                quotes = (type(value) == str)
                self.help_test_update(classname, uid, attr,
                                      value, quotes, False)
                self.help_test_update(classname, uid, attr,
                                      value, quotes, True)
            pass
            if classname == "BaseModel":
                continue
            for attr, attr_type in self.attributes()[classname].items():
                if attr_type not in (str, int, float):
                    continue
                self.help_test_update(classname, uid, attr,
                                      self.attribute_values[attr_type],
                                      True, False)
                self.help_test_update(classname, uid, attr,
                                      self.attribute_values[attr_type],
                                      False, True)

    def help_test_update(self, classname, uid, attr, val, quotes, func):
        """Tests update commmand."""
        #  print("QUOTES", quotes)
        FileStorage._FileStorage__objects = {}
        if os.path.isfile("file.json"):
            os.remove("file.json")
        uid = self.create_class(classname)
        value_str = ('"{}"' if quotes else '{}').format(val)
        if func:
            cmd = '{}.update("{}", "{}", {})'
        else:
            cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, attr, value_str)
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd(cmd)
        fnmsg = fnf.getvalue()[:-1]
        # print("MSG::", fnmsg)
        # print("CMD::", cmd)
        self.assertEqual(len(fnmsg), 0)
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        fns = fnf.getvalue()
        self.assertIn(str(val), fns)
        self.assertIn(attr, fns)

    def test_do_update_error(self):
        """Tests update command with errors."""
        uid = self.create_class("BaseModel")
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("update")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("update garbage")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("update BaseModel")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("update BaseModel 6534276893")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd('update BaseModel {}'.format(uid))
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** attribute name missing **")

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd('update BaseModel {} name'.format(uid))
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** value missing **")

    def test_do_update_error_advanced(self):
        """Tests update() command with errors."""
        uid = self.create_class("BaseModel")
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd(".update()")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("garbage.update()")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("BaseModel.update()")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("BaseModel.update(6534276893)")
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd('BaseModel.update("{}")'.format(uid))
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** attribute name missing **")

        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd('BaseModel.update("{}", "name")'.format(uid))
        fnmsg = fnf.getvalue()[:-1]
        self.assertEqual(fnmsg, "** value missing **")

    def create_class(self, classname):
        """Creates a class for console tests."""
        with patch('sys.stdout', new=StringIO()) as fnf:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = fnf.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)
        return uid

    def help_load_dict(self, rep):
        """Helper method to test dictionary equality."""
        rex = re.compile(r"^\[(.*)\] \((.*)\) (.*)$")
        res = rex.match(rep)
        self.assertIsNotNone(res)
        fns = res.group(3)
        fns = re.sub(r"(datetime\.datetime\([^)]*\))", "'\\1'", fns)
        fnd = json.loads(fns.replace("'", '"'))
        return fnd

    def classes(self):
        """Returns a dictionary of valid classes and their references."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return classes

    def attributes(self):
        """Returns the valid attributes and their types for classname."""
        attributes = {
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str},
            "State":
                     {"name": str},
            "City":
                     {"state_id": str,
                      "name": str},
            "Amenity":
                     {"name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
                     {"place_id": str,
                      "user_id": str,
                      "text": str}
        }
        return attributes


if __name__ == "__main__":
    unittest.main()
