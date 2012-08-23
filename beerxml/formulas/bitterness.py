# -*- coding: utf-8 -*-
#
# This file contains formulas for calculating
# bitterness by the three most popular ibu equations,
# Tinseth, Rager and Garetz
#
# Resources:
# http://www.realbeer.com/hops/
# https://docs.google.com/viewer?url=http://www.nthba.org/www/docs/Brew%2520Day%2520Presentation%2520-%2520Hop%2520Bittering.ppt&pli=1
#

class Tinseth:
    """
    Estimating IBUs Tinseth Formula
    """
    def ibu(self, alpha_acid_utilization, mg_alpha_acids):
        """
        IBUs = decimal alpha acid utilization * mg/l of added alpha acids
        """
        return  alpha_acid_utilization * mg_alpha_acids
    
    def mg_alpha_acids(self, alpha_acid_rating, grams_of_hop, batch_size):
        """
        Calculate the concentration of alpha acids you add to the wort.
        
        mg per litre of added alpha acids = decimal AA rating * grams hops * 1000
                                            -------------------------------------
                                              volume of finished beer in liters
        """
        return alpha_acid_rating * grams_of_hop * 1000 / batch_size
    
    def alpha_acid_utilization(self, bigness_factor, boil_time_factor):
        """
        Calculate alpha acid utilization.
        decimal alpha acid utilization = Bigness factor * Boil Time factor
        """ 
        return bigness_factor * boil_time_factor
    
    def bigness_factor(self, wort_gravity):
        """
        The Bigness factor accounts for reduced utilization due to 
        higher wort gravities. Use an average gravity value for the 
        entire boil to account for changes in the wort volume.
        
        Bigness factor = 1.65 * 0.000125^(wort gravity - 1)
        """
        return 1.65 * 0.000125 ** (float(wort_gravity) -1.0)
    
    def boil_time_factor(self, time_in_mins):
        """
        The Boil Time factor accounts for the change in utilization due to boil time:
        
        Boil Time factor = 1 - e^(-0.04 * time in mins)
                           --------------------------
                                       4.15
        """
        e = 2.71828182846
        return 1 - e ** (-0.04 * float(time_in_mins)) / 4.15


class Rager:
    """
    Estimating IBUs Rager Formula
    
    IBU = %U * Woz * %A * 7462
          --------------------
            Vgal * (1 + GA)
            
    Where:
        GA = (GB – 1.050)/.2
    
    GB = Gravity of boiling wort at end of boil
    GA = Gravity adjustment
    Woz = Hop weight in ounces
    Vgal = Volume of beer fermented in gallons
    %U = Boil utilization percent
    %A = Hop alpha acid percent
    """
    pass

class Garetz:
    """
    Estimating IBUs Garetz Formula
    
    IBU =    %U * Woz * %A * 7490
          --------------------------
           Vgal * (1 + GA) * TF * HF
    
    Where:
        GA = (GB – 1.050)/.2
        
    TF = ((Elevation in feet/550)*0.02) + 1
    CF = (Ferment Vol)/(Boil Vol)
    HF = (CF*IBU/260) + 1
    """
    pass