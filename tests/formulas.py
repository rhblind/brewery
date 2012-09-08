# -*- coding: utf-8 -*-

from django.test import TestCase
from brewery.beerxml.formulas import bitterness


class BitternessTestCase(TestCase):
    """
    Test the various bitterness formulas.
    Note: floats are a bit tricky to test, so
    we use some Internet tricks to 'sort-of' test them
    """
    
    def setUp(self):
        self.boil_time_minutes = 60.0
        self.wort_gravity = 1.34
        
        
    def test_tinseth_boil_time_factor(self):
        tinseth = bitterness.Tinseth()
        btf = tinseth.boil_time_factor(self.boil_time_minutes)
        
        diff = abs(btf - 0.978140252219)
        delta = 0.000000000001
        self.assertTrue(diff < delta,
                "difference: %s is not less than %s" % (diff, delta))