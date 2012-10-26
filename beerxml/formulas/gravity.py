# -*- coding: utf-8 -*-
#
# References:
# http://hbd.org/ensmingr/
# http://en.wikipedia.org/wiki/Brix
# http://realbeer.com/spencer/attenuation.html
# http://en.wikipedia.org/wiki/Gravity_(alcoholic_beverage)
# http://morebeer.com/brewingtechniques/library/backissues/issue2.1/manning.html

def plato_to_gravity(degrees_plato):
    """
    Convert degrees plato to gravity.
    """
    return 259.0 / (259.0 - degrees_plato)

def gravity_to_plato(gravity):
    """
    Convert gravity to degrees plato.
    """
    return 259.0 - (259.0 / gravity)

def gravity_to_brix(gravity):
    """
    Convert gravity to degrees brix
    """
    return (((182.4601 * gravity - 775.6821) * gravity \
             + 1262.7794) * gravity - 669.5622)
    
def brix_to_gravity(brix):
    """
    Convert degrees brix to gravity
    """
    # TODO: implement
    pass

def specific_gravity(original_gravity, final_gravity):
    """
    The percentage of alcohol can be calculated from the 
    difference between the original gravity of the wort 
    and the current specific gravity of wort.
    """
    return ((1.05 * (original_gravity - final_gravity) / final_gravity) / 0.79)

def alcohol_by_volume(original_gravity, final_gravity):
    """
    Calculate the Alcohol By Volume (ABV).
    """
    return (original_gravity - final_gravity) / 0.75

def alcohol_by_weight(alcohol_by_volume, final_gravity=None):
    """
    Calculate the Alcohol By Weight (ABW).
    If the final gravity is not know, but has "normal" levels
    of alcohol and attenuation, the ABW can be calculated
    using this formula: (0.78 * alcohol_by_volume)
    """
    if final_gravity is not None:
        return (0.79 * alcohol_by_volume) / final_gravity
    return (0.78 * alcohol_by_volume)
    
def true_extract(original_gravity, final_gravity):
    """
    
    """
    return 0.1808 * original_gravity + 0.8192 * final_gravity

def alcohol_content():
    pass

def apparent_attenuation():
    pass

def true_attenuation(original_gravity, final_gravity):
    """

    """
    return 1 - true_extract(original_gravity, final_gravity) \
         / original_gravity

def brewers_point():
    pass