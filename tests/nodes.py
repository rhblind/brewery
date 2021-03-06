# -*- coding: utf-8 -*-

import os
from django.test import TestCase
from django.db.models.base import Model

from brewery.beerxml import parser
from brewery.beerxml.nodes import BeerXMLNode
from brewery.tests import FILES, EXAMPLES_DIR

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
    
    def test_get_or_create(self):
        """
        test the get_or_create() method on
        BeerXMLNode, which are used to save new
        recipes to database
        """
        for f in FILES:
            with open(os.path.join(EXAMPLES_DIR, f), "r") as fname:
                nodetree = parser.to_beerxml(fname)
                for nodelist in nodetree.itervalues():
                    for node in nodelist:
                        self.assertIsInstance(node, BeerXMLNode, "is not a BeerXMLNode instance")
                        obj, created = node.get_or_create()
                        self.assertIsInstance(obj, Model, "is not a model instance")
                        self.assertTrue(created, "was not created")
