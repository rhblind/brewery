# -*- coding: utf-8 -*-
#
# References:
# http://hbd.org/ensmingr/
# http://plato.montanahomebrewers.org/
# http://en.wikipedia.org/wiki/Gravity_(alcoholic_beverage)
# http://morebeer.com/brewingtechniques/library/backissues/issue2.1/manning.html

def plato_to_gravity(degrees_plato):
    """
    Convert degrees plato to specific gravity.
    """
    return 259.0 / (259.0 - degrees_plato)

def gravity_to_plato(specific_gravity):
    """
    Convert specific gravity to degrees plato.
    """
    return 259.0 - (259.0 / specific_gravity)
    
def specific_gravity(original_gravity, final_gravity):
    """
    The percentage of alcohol can be calculated from the 
    difference between the original gravity of the wort 
    and the current specific gravity of wort.
    """
    pass

def original_extract():
    pass


def apparent_extract():
    pass

def true_extract():
    pass

def alcohol_content():
    pass

def attenuation():
    pass

def brewers_point():
    pass