# -*- coding: utf-8 -*-

import os

EXAMPLES_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                            "beerxml-examples")
FILES = ("equipment.xml", "grain.xml", "hops.xml", "mash.xml",
         "misc.xml", "recipes.xml", "style.xml", "water.xml", 
         "yeast.xml")

__all__ = ("EXAMPLES_DIR", "FILES")

print EXAMPLES_DIR

from brewery.tests.parser import *
from brewery.tests.nodes import *
from brewery.tests.formulas import *