# -*- coding: utf-8 -*-

import os
from django.test import TestCase

from brewery.beerxml import parser
from brewery.tests import FILES, EXAMPLES_DIR

class BeerXMLParserTestCase(TestCase):
    """
    Test the beerxml parser
    """
    def test_examples_exists(self):
        """
        Make sure all example files exists and are readable
        """
        for f in FILES:
            with open(os.path.join(EXAMPLES_DIR, f), "r") as fname:
                # will throw IOError if file does not exist
                fname.close()
    
    def test_to_tuple_as_str(self):
        """
        Test to_tuple method on all example files
        as xml string object
        """
        for f in FILES:
            with open(os.path.join(EXAMPLES_DIR, f), "r") as fname:
                xml_str = fname.read()               # test xml as str
                self.assertIsInstance(xml_str, str)  # make sure xml is str
                parser.to_tuple(xml_str)
    
    def test_to_tuple_as_file(self):
        """
        Test to_tuple method on all example files
        as xml string object
        """
        for f in FILES:
            with open(os.path.join(EXAMPLES_DIR, f), "r") as fname:
                self.assertIsInstance(fname, file)  # make sure fname is file
                parser.to_tuple(fname)
                
    def test_to_dict_as_str(self):
        """
        Test to_tuple method on all example files
        as xml string object
        """
        for f in FILES:
            with open(os.path.join(EXAMPLES_DIR, f), "r") as fname:
                xml_str = fname.read()               # test xml as str
                self.assertIsInstance(xml_str, str)  # make sure xml is str
                parser.to_dict(xml_str)
    
    def test_to_dict_as_file(self):
        """
        Test to_tuple method on all example files
        as xml string object
        """
        for f in FILES:
            with open(os.path.join(EXAMPLES_DIR, f), "r") as fname:
                self.assertIsInstance(fname, file)  # make sure fname is file
                parser.to_dict(fname)
                
    def test_to_beerxml_as_str(self):
        """
        Test to_tuple method on all example files
        as xml string object
        """
        for f in FILES:
            with open(os.path.join(EXAMPLES_DIR, f), "r") as fname:
                xml_str = fname.read()               # test xml as str
                self.assertIsInstance(xml_str, str)  # make sure xml is str
                parser.to_beerxml(xml_str)
    
    def test_to_beerxml_as_file(self):
        """
        Test to_tuple method on all example files
        as xml string object
        """
        for f in FILES:
            with open(os.path.join(EXAMPLES_DIR, f), "r") as fname:
                self.assertIsInstance(fname, file)  # make sure fname is file
                parser.to_beerxml(fname)


                