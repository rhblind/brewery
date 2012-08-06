# -*- coding: utf-8 -*-
#
# Tests for the brewery app
#

import os
from django.test import TestCase

from beerxml import parser
from beerxml.models import BeerXMLNode

EXAMPLES_DIR = os.path.join("docs", "beerxml-examples")
FILES = ("equipment.xml", "grain.xml", "hops.xml", "mash.xml",
         "misc.xml", "recipes.xml", "style.xml", "water.xml",
         "yeast.xml")

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
    
    
class BeerXMLNodeTestCase(TestCase):
    """
    Test the BeerXMLNode class
    """
    def test_beerxml_node_dict_methods(self):
        """
        Make sure all expected dict methods work
        """
        for f in FILES:
            with open(os.path.join(EXAMPLES_DIR, f), "r") as fname:
                nodetree = parser.to_beerxml(fname)
                for node in nodetree.itervalues():
                    # Only test the actual BeerXMLNodes, not
                    # the collections which can be in it for
                    # related fields
                    if isinstance(node, BeerXMLNode):

                        # test some iterators
                        iter(node)
                        node.items()
                        node.iteritems()
                        node.keys()
                        node.iterkeys()
                        node.values()
                        node.itervalues()
                        
                        # test various dict setter and getters methods
                        node["spam"] = "eggs"
                        self.assertEqual(node["spam"], "eggs")
                    
                        node.update({"spam": "rat"})
                        self.assertEqual(node["spam"], "rat")
                        
                        node.update(strawberry="tart", brain="hurts")
                        self.assertEqual(node["strawberry"], "tart")
                        self.assertEqual(node["brain"], "hurts")
                        
                        node.update({"nobody_expects": "the Spanish inquisition"},
                                    nipples="explodes with delight!")
                        self.assertEqual(node["nobody_expects"], "the Spanish inquisition")
                        self.assertEqual(node["nipples"], "explodes with delight!")
                        
                        node.update({"nights_of": 9}, heads=3)
                        self.assertEqual(node["nights_of"], 9)
                        self.assertEqual(node["heads"], 3)
                        
                        node.setdefault("rats", 6)
                        self.assertEqual(node["rats"], 6)
                        
                        node.setdefault("brave_sir_knight")
                        self.assertEqual(node["brave_sir_knight"], None)
                        
                        # test other dict methods
                        self.assertTrue(node.has_key("brave_sir_knight"))
                        self.assertEqual(node.get("rats"), 6)
                        
                        
                        
                        
                        
                        
                        
                        
                        
                    