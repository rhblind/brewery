# -*- coding: utf-8 -*-
#
# This file contains formulas for calculating
# bitterness by the three most popular ibu equations,
# Tinseth, Rager and Garetz
#
# Resources:
# http://www.realbeer.com/hops/
# http://www.realbeer.com/hops/FAQ.html
# https://docs.google.com/viewer?url=http://www.nthba.org/www/docs/Brew%2520Day%2520Presentation%2520-%2520Hop%2520Bittering.ppt&pli=1

import math

class Tinseth:
    """
    Estimating IBUs using Tinseth's equations.
    """
    def ibu(self, alpha_acid_utilization, mg_alpha_acids):
        """
        IBUs = decimal alpha acid utilization * mg/l of added alpha acids.
        """
        return  alpha_acid_utilization * mg_alpha_acids
    
    def mg_alpha_acids(self, alpha_acid_rating, grams_of_hop, batch_size_liters):
        """
        Calculate the concentration of alpha acids you add to the wort using
        metric system.
        """
        return alpha_acid_rating * grams_of_hop * 1000 / batch_size_liters
    
    def mg_alpha_acids_non_metric(self, alpha_acid_rating, ounces_of_hop, 
                                  batch_size_gallons):
        """
        Calculate the concentration of alpha acids you add to the wort using
        non-metric system.
        """
        return alpha_acid_rating * ounces_of_hop * 7490 / batch_size_gallons
    
    def alpha_acid_utilization(self, bigness_factor, boil_time_factor):
        """
        Calculate alpha acid utilization.
        """ 
        return bigness_factor * boil_time_factor
    
    def bigness_factor(self, wort_gravity):
        """
        The Bigness factor accounts for reduced utilization due to 
        higher wort gravities. Use an average gravity value for the 
        entire boil to account for changes in the wort volume.
        """
        return 1.65 * 0.000125 ** (float(wort_gravity) -1.0)
    
    def boil_time_factor(self, time_in_minutes):
        """
        The boil time factor accounts for the change in utilization due 
        to boil time.
        """
        e = 2.71828182846
        return 1 - e ** (-0.04 * float(time_in_minutes)) / 4.15


class Rager:
    """
    Estimate IBUs using Rager's equations.
    """
    
    def ibu(self, grams_of_hop, utilization_percentage, alpha_acid_percentage,
            batch_size_liters, gravity_adjustment):
        """
        Calculate IBU using metric units.
        """
        return grams_of_hop * utilization_percentage * alpha_acid_percentage \
                * 1000 / batch_size_liters * (1 + gravity_adjustment)
                
    def ibu_non_metric(self, ounces_of_hop, utilization_percentage, 
               alpha_acid_percentage, batch_size_gallons, gravity_adjustment):
        """
        Calculate IBU using non-metric units.
        """
        return ounces_of_hop * utilization_percentage * alpha_acid_percentage \
                * 7462 / batch_size_gallons * (1 + gravity_adjustment)
        
    def utilization_percentage(self, time_in_minutes):
        """
        Calculate the alpha acid utilization percentage.
        """
        return 18.11 + 13.86 * math.tanh((time_in_minutes - 31.32) / 18.27)
    
    def gravity_adjustment(self, boil_gravity):
        """
        According to Rager, if the gravity of the boil exceeds 1.050, 
        there is a gravity adjustment (GA) to factor in.
        """
        return (boil_gravity - 1.050) / 0.2 if boil_gravity > 1.050 else 0
    
    
class Garetz:    
    """
    Estimate IBUs using Garetz' equations.
    """
    
    def ibu(self, grams_of_hop, utilization_percentage, alpha_acid_percentage, 
            batch_size_liters, combined_adjustments):
        """
        Calculate IBUs using metric units.
        """
        return grams_of_hop * utilization_percentage * alpha_acid_percentage \
                * 0.1 / batch_size_liters * combined_adjustments
    
    def ibu_non_metric(self, ounces_of_hop, utilization_percentage, 
               alpha_acid_percentage, batch_size_gallons, combined_adjustments):
        """
        Calculate IBUs using non-metric units.
        """
        return ounces_of_hop * utilization_percentage * alpha_acid_percentage \
                * 0.749 / batch_size_gallons * combined_adjustments
    
    def combined_adjustments(self, gravity_factor, hopping_rate_factor, 
                             temperature_factor):
        """
        According to Garetz, there are several adjustment factors, 
        that he brings together in the formula with the term 
        "combined adjustments" (CA)
        """
        return gravity_factor * hopping_rate_factor * temperature_factor
    
    def concentration_factor(self, final_volume, boil_volume):
        """
        Calculate the concentration factor to account for extract brews.
        """
        return final_volume / boil_volume
    
    def boil_gravity(self, concentration_factor, starting_gravity):
        """
        Calculate boil gravity.
        """
        return (concentration_factor * (starting_gravity -1)) + 1
    
    def gravity_factor(self, boil_gravity):
        """
        Calculate gravity factor.
        """
        return (boil_gravity - 1.050 / 0.2) + 1
    
    def hopping_rate_factor(self, concentration_factor, desired_ibu):
        """
        Calculate hopping rate factor.
        """
        return ((concentration_factor * desired_ibu) / 260) + 1
        
    def temperature_factor(self, elevation_in_feet):
        """
        Calculate temperature factor
        """
        return ((elevation_in_feet / 550) * 0.02) + 1
    
    