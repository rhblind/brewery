# -*- coding: utf-8 -*-
#
# This file contains formulas for calculating
# bitterness by the three most popular ibu equations,
# Tinseth, Rager and Garetz
#

class Tinseth:
    """
    Calculate bitterness by Tinseth's approximation
    All formula's from http://www.realbeer.com/hops/research.html
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
    pass


class Garetz:
    pass