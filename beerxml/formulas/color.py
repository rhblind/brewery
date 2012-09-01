# -*- coding: utf-8 -*-
#
# References
# http://brewwiki.com/
# http://beersmith.com/blog/2008/04/29/beer-color-understanding-srm-lovibond-and-ebc/
# http://www.babblehomebrewers.com/attachments/article/61/BeerColor.pdf
#
# The Standard Reference Method, abbreviated as SRM is the color 
# system used by brewers to specify finished beer and malt color. 
# In the case of malt it is actually the SRM color of a laboratory 
# wort made from the malt which is printed on the package. The SRM 
# value is 12.7 times the log of the attenuation experienced by 
# light of wavelength 430 nanometers (deep blue) in passing through 
# 1 cm of the beer (or wort). The scaling factor (12.7) and path were 
# chosen (1951) to make SRM values correspond closely to values measured 
# in the Lovibond system which was in use at the time. The two systems are 
# approximately equivalent for home brewing applications.

def mcu(grain_color_lovibond, grain_weight_lbs, volume_gallons):
    """
    The simplest equation for estimating the color 
    of beer is to use Malt Color Units (MCU). A malt 
    color unit is defined to be simply the color of 
    each grain times the grain weight in pounds divided by 
    the batch volume in gallons. If more than one grain is used, 
    the MCU color is calculated for each addition and then 
    added together. This malt color unit equation provides a 
    good estimate of color in SRM for beers that are light in 
    color (SRM color < 10.5).
    """
    return (grain_color_lovibond * grain_weight_lbs) / volume_gallons

def srm_to_ebc(srm):
    """
    Convert from Standard Reference Method (SRM) color system to
    European Brewing Convention (EBC) color system.
    """
    return 1.97 * srm
     
def mosher(mcu):
    """
    Return Standard Reference Method (SRM) using Mosher's 
    approximation.
    
    Randy Mosher developed a model based on commercial beers 
    whose recipes and color were known.
    Using this approximation, minimum beer color is 4.7. 
    This is not realistic and the model should only be used for 
    beer with MCU greater than 7.
    """
    return (0.3 * mcu) + 4.7

def daniels(mcu):
    """
    Return Standard Reference Method (SRM) using Daniels' 
    approximation.
    
    Daniels’ model differs from Mosher’s and suggests that 
    homebrew is generally darker than commercial beers.
    Like Mosher’s model, the formula has a minimum color that 
    is not reasonable. Consequently the formula should only 
    be used for beers with MCU greater than 11.
    """
    return (0.2 * mcu) + 8.4
    
def morey(mcu):
    """
    Return Standard Reference Method (SRM) using Morey's 
    approximation.
    
    Morey's approximation is based on five assumptions.
    
    1. SRM is approximately equal to MCU for values from 0 to 10.
    2. Homebrew is generally darker than commercial beer.
    3. Base on the previous qualitative postulate, Morey assumed that 
       Ray Daniels’ predicted relationship exists for beers with color 
       greater than 10.
    4. Since Mosher’s equation predicts darker color than Daniels’ model 
       for values of MCU greater than 37, Morey assumed that Mosher’s 
       approximation governed beer color for all values more than 37 MCUs.
    5. Difference in color for beers greater than 40 SRM are essentially 
       impossible to detect visually; therefore, Morey limited the 
       analysis to SRM of 50 and less.
    """
    return 1.4922 * (mcu ** 0.6859)
    
