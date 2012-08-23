# -*- coding: utf-8 -*-
#
#===============================================================================
# Not exactly PEP8 compliant, but so be it... 
# 
# _beerxml_attrs:
#  All field names try to follow the naming convention from beerxml
#  unless field name is a reserved python word. If field is a reserved
#  word, model should include a dict  _beerxml_attrs = {"beerxml_name" : "model_name",}
#  for each field not following the beerxml standard.
#
# BeerXML reference
#  - http://www.beerxml.com/beerxml.htm
#
# Data formats:
# All DecimalFields are this big to support scientific input numbers
#  - Record         : Model (database table)
#  - Text           : CharField or TextField dependent on situation
#  - Integer        : IntegerField (may include negative values, 
#                     except version which is PositiveSmallIntegerField)
#  - Percentage     : DecimalField (max digits: 14, decimal places: 9 = max val 99999.999999999)
#  - Weight         : DecimalField (max_digits: 14, decimal_places: 9 = max val 99999.999999999)
#  - Temperature    : DecimalField (max_digits: 14, decimal_places: 9 = max val 99999.999999999)
#  - List           : CharField with choices (key=numeric index, value=display value)
#  - Time           : DecimalField (max_digits: 14, decimal_places: 9 = max val 99999.999999999)
#  - Floating Point : DecimalField (max_digits: 14, decimal_places: 9 = max val 99999.999999999)
#  - Boolean        : BooleanField
#
#
# Units:
#  The following units are allowed and may be used interchangeably. However, only units of 
#  the appropriate type may be used for a given value. For example "volume" units may not be 
#  used for "Weight" fields.
#
#  Weight Units
#    kg - Kilograms g - Grams
#    oz - Ounces
#    lb – Pounds
#
#  Volume Units
#    tsp – Teaspoons tblsp – Tablespoons oz – Ounces (US) cup – Cups (US)
#    pt – Pints (US)
#    qt – Quarts (US)
#    ml - Milliliters
#    l – Liters
#
#  Temperature Units
#    F – Degrees Fahrenheit C – Degrees Celsius
#    Time Units
#    min - Minutes hour - Hours day – Days week – Weeks
#
#  Color Units
#    srm – SRM Color ebc – EBC Color
#    L – Degrees lovibond.
#
#  Specific Gravity Units
#    sg – The relative gravity by weight when compared to water. For example “1.035 sg” 
#    plato – Gravity measured in degrees plato
#===============================================================================

from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.dispatch.dispatcher import receiver
from django.template.defaultfilters import slugify



#
# Models
#

class BeerXMLBase(models.Model):
    """
    Base model which all other models inherit
    from. This model has fields and methods which
    are common for all models
    """

    class Meta:
        abstract = True
        app_label = "brewery"
        
    name = models.CharField(_("name"), max_length=100)
    version = models.PositiveSmallIntegerField(_("version"), default=1,
                                        editable=False, help_text="XML version")
    slug = models.SlugField(max_length=100, blank=True)
    registered_by = models.ForeignKey(User, blank=True, null=True,
            related_name="%(app_label)s_%(class)s_registered_by_set", help_text="Registered by")
    modified_by = models.ForeignKey(User, blank=True, null=True,
            related_name="%(app_label)s_%(class)s_modified_by_set", help_text="Modified by")
    cdt = models.DateTimeField(_("created"), editable=False, auto_now_add=True)
    mdt = models.DateTimeField(_("modified"), editable=False, auto_now=True)
    
            
class Equipment(BeerXMLBase):
    """
    Database model for equipment
    """

    boil_size = models.DecimalField(_("boil size"), max_digits=14, 
            decimal_places=9, help_text="""The pre-boil volume used in this 
            particular instance for this equipment setup. Note that this may 
            be a calculated value depending on the CALC_BOIL_VOLUME parameter.""")
    batch_size = models.DecimalField(_("batch size"), max_digits=14, 
            decimal_places=9, help_text="""The target volume of the batch at the 
            start of fermentation.""")
    tun_volume = models.DecimalField(_("tun volume (litres)"), max_digits=14,
            decimal_places=9, blank=True, null=True, help_text="""Volume of the 
            mash tun in liters. This parameter can be used to calculate if a 
            particular mash and grain profile will fit in the mash tun. It may also 
            be used for thermal calculations in the case of a partially full 
            mash tun.""")
    tun_weight = models.DecimalField(_("tun weight (kilos)"), max_digits=14,
            decimal_places=9, blank=True, null=True, help_text="""Weight of the 
            mash tun in kilograms. Used primarily to calculate the thermal parameters 
            of the mash tun – in conjunction with the volume and specific heat.""")
    tun_specific_heat = models.DecimalField(_("tun specific heat (cal/(g*K))"), 
            max_digits=14, decimal_places=9, blank=True, null=True, help_text="""The 
            specific heat of the mash tun which is usually a function of the material 
            it is made of. Typical ranges are 0.1-0.25 for metal and 0.2-0.5 for 
            plastic materials.""")
    top_up_water = models.DecimalField(_("top-up water"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""The amount of top 
            up water normally added just prior to starting fermentation. Usually 
            used for extract brewing.""")
    trub_chiller_loss = models.DecimalField(_("trub chiller loss"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""The amount of wort 
            normally lost during transition from the boiler to the fermentation vessel. 
            Includes both unusable wort due to trub and wort lost to the chiller and 
            transfer systems.""")
    evap_rate = models.DecimalField(_("evaporation rate (% per hour)"), 
            max_digits=14, decimal_places=9, blank=True, null=True, help_text="""The 
            percentage of wort lost to evaporation per hour of the boil.""")
    boil_time = models.DecimalField(_("boil time (hours,minutes)"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""The normal amount of 
            time one boils for this equipment setup. This can be used with the 
            evaporation rate to calculate the evaporation loss.""")
    calc_boil_volume = models.BooleanField(_("calculate boil volume"), default=False, 
            help_text="""Flag denoting that the program should calculate the boil size. 
            Flag may be True or False. If set then the boil size should match this value.""")
    lauter_deadspace = models.DecimalField(_("lauter deadspace (litres)"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""Amount lost to 
            the lauter tun and equipment associated with the lautering process.""")
    top_up_kettle = models.DecimalField(_("kettle top-up water (litres)"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""Amount normally added 
            to the boil kettle before the boil.""")
    hop_utilization = models.DecimalField(_("hop utilization %"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""Large batch hop 
            utilization. This value should be 100% for batches less than 20 gallons, 
            but may be higher (200% or more) for very large batch equipment.""")
    notes = models.TextField(_("notes"), blank=True, null=True)
    
    # Optional extension for BeerXML display
    display_boil_size = models.CharField(_("display boil size"), max_length=50, 
            blank=True, null=True, help_text="""The pre-boil volume normally 
            used for a batch of this size shown in display volume units such 
            as “5.5 gal”""")
    display_batch_size = models.CharField(_("display batch size"), max_length=50, 
            blank=True, null=True, help_text="""The target volume of the batch 
            at the start of fermentation in display volume units such as “5.0 gal”""")
    display_tun_volume = models.CharField(_("display tun volume"), max_length=50, 
            blank=True, null=True, help_text="""Volume of the mash tun in display 
            units such as “10.0 gal” or “20.0 l”""")
    display_tun_weight = models.CharField(_("display tun weight"), max_length=50, 
            blank=True, null=True, help_text="""Weight of the mash tun in display 
            units such as “3.0 kg” or “6.0 lb”""")
    display_top_up_water = models.CharField(_("display top up water"), max_length=50, 
            blank=True, null=True, help_text="""The amount of top up water 
            normally added just prior to starting fermentation in display volume 
            such as “1.0 gal”""")
    display_trub_chiller_loss = models.CharField(_("display trub chiller loss"), 
            max_length=50, blank=True, null=True, help_text="""The amount of wort 
            normally lost during transition from the boiler to the fermentation 
            vessel. Includes both unusable wort due to trub and wort lost to the 
            chiller and transfer systems. Expressed in user units - Ex: “1.5 qt”""")
    display_lauter_deadspace = models.CharField(_("display lauter deadspace"), 
            max_length=50, blank=True, null=True, help_text="""Amount lost to the 
            lauter tun and equipment associated with the lautering process. 
            Ex: “2.0 gal” or “1.0 l”""")
    display_top_up_kettle = models.CharField(_("display top up kettle"), 
            max_length=50, blank=True, null=True, help_text="""Amount normally 
            added to the boil kettle before the boil. Ex: “1.0 gal”""")
    
    def __unicode__(self):
        return u"%s" % self.name
    
    @property
    def boil_volume(self):
        return (self.batch_size - self.top_up_water - self.trub_chiller_loss) \
                * (1 + self.boil_time * self.evap_rate)
                
    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.calc_boil_volume is True:
            self.boil_size = self.boil_volume
      
            
class Fermentable(BeerXMLBase):
    """
    The term "fermentable" encompasses all fermentable items that contribute 
    substantially to the beer including extracts, grains, sugars, honey, fruits.
    """
    
    TYPE = (
        (u"grain", u"Grain"),
        (u"sugar", u"Sugar"),
        (u"extract", u"Extract"),
        (u"dry extract", u"Dry extract"),
        (u"adjunct", u"Adjunct")
    )
    
    # NOTE: type is a reserved python word.
    ferm_type = models.CharField(_("fermentable type"), max_length=12, choices=TYPE)
    amount = models.DecimalField(_("amount"), max_digits=14, decimal_places=9,
            help_text="Weight of the fermentable, extract or sugar in Kilograms.")
    # NOTE: yield is a reserved python word.
    ferm_yield = models.DecimalField(_("yield percentage"), max_digits=14, 
            decimal_places=9, help_text="""Percent dry yield (fine grain) 
            for the grain, or the raw yield by weight if this is an 
            extract adjunct or sugar.""")
    color = models.DecimalField(_("color"), max_digits=14, decimal_places=9,
            help_text="""The color of the item in Lovibond Units 
            (SRM for liquid extracts).""")
    add_after_boil = models.BooleanField(_("add after boil"), default=False,
            help_text="""May be TRUE if this item is normally added after 
            the boil. The default value is FALSE since most grains are added 
            during the mash or boil.""")
    origin = models.CharField(_("origin country"), max_length=100, blank=True, null=True)
    supplier = models.TextField(_("supplier"), blank=True, null=True)
    notes = models.TextField(_("notes"), blank=True, null=True)
    coarse_fine_diff = models.DecimalField(_("coarse/fine percentage"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""Percent difference 
            between the coarse grain yield and fine grain yield.  Only appropriate for 
            a "Grain" or "Adjunct" type, otherwise this value is ignored.""")
    moisture = models.DecimalField(_("moisture percentage"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""Percent 
            moisture in the grain. Only appropriate for a "Grain" or "Adjunct" type, 
            otherwise this value is ignored.""")
    diastatic_power = models.DecimalField(_("diastatic power"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""The diastatic power 
            of the grain as measured in "Lintner" units. Only appropriate for a 
            "Grain" or "Adjunct" type, otherwise this value is ignored.""")
    protein = models.DecimalField(_("protein percentage"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""The percent 
            protein in the grain. Only appropriate for a "Grain" or "Adjunct" type, 
            otherwise this value is ignored.""")
    max_in_batch = models.DecimalField(_("max percentage per batch"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""The recommended 
            maximum percentage (by weight) this ingredient should represent in a 
            batch of beer.""")
    recommend_mash = models.NullBooleanField(_("recommended mash"), default=False, 
            blank=True, null=True, help_text="""True if it is recommended the grain 
            be mashed, False if it can be steeped. A value of True is only appropriate 
            for a "Grain" or "Adjunct" types. The default value is False. Note that 
            this does NOT indicate whether the grain is mashed or not – it is only 
            a recommendation used in recipe formulation.""")
    ibu_gal_per_lb = models.DecimalField(_("bitterness (IBU*gal/lb)"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""For hopped extracts 
            only - an estimate of the number of IBUs per pound of extract in a gallon 
            of water. To convert to IBUs we multiply this number by the "Amount" 
            field (in pounds) and divide by the number of gallons in the batch. 
            Based on a sixty minute boil. Only suitable for use with an "Extract" type, 
            otherwise this value is ignored.""")
    
    # Optional extension for BeerXML display
    display_amount = models.CharField(_("display amount"), max_length=50, blank=True, 
            null=True, help_text="""The amount of fermentables in this record along 
            with the units formatted for easy display in the current user defined units. 
            For example “1.5 lbs” or “2.1 kg”.""")
    potential = models.DecimalField(_("potential"), max_digits=14, decimal_places=9, 
            blank=True, null=True, help_text="""The yield of the fermentable converted 
            to specific gravity units for display. For example “1.036” or “1.040” 
            might be valid potentials.""")
    inventory = models.CharField(_("inventory"), max_length=50, blank=True, null=True,
            help_text="""Amount in inventory for this item along with the units 
            – for example “10.0 lb”""")
    display_color = models.CharField(_("display color"), max_length=50, blank=True, 
            null=True, help_text="""Color in user defined color units along with the 
            unit identified – for example “200L” or “40 ebc""")
    
    _beerxml_attrs = {
        "type": "ferm_type",
        "yield": "ferm_yield"
    }
    
    def __unicode__(self):
        return u"%s" % self.name

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.ferm_type:
            self.ferm_type = u"%s" % self.ferm_type.lower()
    
    
class Hop(BeerXMLBase):
    """
    The “Hop” identifier is used to define all varieties of hops.
    """
    USE = (
        (u"boil", u"Boil"),
        (u"dry hop", u"Dry Hop"),
        (u"mash", u"Mash"),
        (u"first wort", u"First Wort"),
        (u"aroma", u"Aroma")
    )
    
    TYPE = (
        (u"bittering", u"Bittering"),
        (u"aroma", u"Aroma"),
        (u"both", u"Both")
    )
    
    FORM = (
        (u"pellet", u"Pellet"),
        (u"plug", u"Plug"),
        (u"leaf", u"Leaf")
    )
    
    alpha = models.DecimalField(_("alpha percentage"), max_digits=14, 
            decimal_places=9, help_text="""Percent alpha of hops 
            - for example "5.5" represents 5.5% alpha""")
    amount = models.DecimalField(_("amount"), max_digits=14, decimal_places=9,
            help_text="Weight in Kilograms of the hops used in the recipe.")
    use = models.CharField(_("usage"), max_length=12, choices=USE,
            help_text="""Note that Aroma and Dry Hop do not contribute to the 
            bitterness of the beer while the others do.  Aroma hops are added 
            after the boil and do not contribute substantially to beer 
            bitterness.""")
    time = models.DecimalField(_("time"), max_digits=14, decimal_places=9,
            help_text="""The time as measured in minutes. Meaning is dependent 
            on the “usage” field. For “Boil” this is the boil time.  For “Mash” 
            this is the mash time. For “First Wort” this is the boil time. 
            For “Aroma” this is the steep time. For “Dry Hop” this is the amount 
            of time to dry hop.""")
    notes = models.TextField(_("notes"), blank=True, null=True)
    # NOTE: type is a reserved python word.
    hop_type = models.CharField(_("hop type"), max_length=12, choices=TYPE, 
                                blank=True, null=True)
    form = models.CharField(_("hop form"), max_length=12, choices=FORM, blank=True, null=True)
    beta = models.DecimalField(_("beta percentage"), max_digits=14, decimal_places=9, 
            blank=True, null=True, help_text="""Hop beta percentage 
            - for example "4.4" denotes 4.4 % beta""")
    hsi = models.DecimalField(_("HSI"), max_digits=14, decimal_places=9, blank=True, 
            null=True, help_text="""Hop Stability Index - defined as the percentage 
            of hop alpha lost in 6 months of storage""")
    origin = models.CharField(_("origin"), max_length=100, blank=True, null=True)
    substitutes = models.TextField(_("substitutes"), blank=True, null=True, 
            help_text="Substitutes that can be used for this hops")
    humulene = models.DecimalField(_("humulene percentage"), max_digits=14, decimal_places=9,
                                   blank=True, null=True)
    caryophyllene = models.DecimalField(_("caryophyllene percentage"), max_digits=14, 
                                        decimal_places=9, blank=True, null=True)
    cohumulone = models.DecimalField(_("cohumulone percentage"), max_digits=14, decimal_places=9,
                                     blank=True, null=True)
    myrcene = models.DecimalField(_("myrcene percentage"), max_digits=14, decimal_places=9,
                                  blank=True, null=True)
    
    # Optional extension for BeerXML display
    display_amount = models.CharField(_("display amount"), max_length=50, 
            blank=True, null=True, help_text="""The amount of hops in this record 
            along with the units formatted for easy display in the current user 
            defined units. For example “100 g” or “1.5 oz”.""")
    inventory = models.CharField(_("inventory"), max_length=50, blank=True, null=True,
            help_text="""Amount in inventory for this item along with the units 
            – for example “10.0 oz.”""")
    display_time = models.CharField(_("display time"), max_length=50, blank=True, null=True,
            help_text="""Time displayed in minutes for all uses except for the dry hop 
            which is in days. For example “60 min”, “3 days”.""")
    
    _beerxml_attrs = {
        "type": "hop_type"
    }
    
    def __unicode__(self):
        return u"%s" % self.name

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.use:
            self.use = u"%s" % self.use.lower()
        if self.hop_type:
            self.hop_type = u"%s" % self.hop_type.lower()
        if self.form:
            self.form = u"%s" % self.use.lower()
    

class MashStep(BeerXMLBase):
    """
    Used within a Mash profile to record the steps
    """
    TYPE = (
        (u"infusion", u"Infusion"),
        (u"temperature", u"Temperature"),
        (u"decoction", u"Decoction")
    )

    # NOTE: type is a reserved python word.
    mash_type = models.CharField(_("type"), max_length=12, choices=TYPE, 
            help_text="""May be “Infusion”, “Temperature” or “Decoction” depending 
            on the type of step. Infusion denotes adding hot water, Temperature 
            denotes heating with an outside heat source, and decoction denotes 
            drawing off some mash for boiling.""")
    infuse_amount = models.DecimalField(_("infuse amount"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""The volume of 
            water in liters to infuse in this step. Required only for infusion steps, 
            though one may also add water for temperature mash steps. One should 
            not have an infusion amount for decoction steps.""")
    step_temp = models.DecimalField(_("step temperature"), max_digits=14, decimal_places=9, 
            help_text="The target temperature for this step in degrees Celsius.")
    step_time = models.DecimalField(_("step time"), max_digits=14, decimal_places=9, 
            help_text="""The number of minutes to spend at this step – i.e. the 
            amount of time we are to hold this particular step temperature.""")
    ramp_time = models.DecimalField(_("ramp time"), max_digits=14, decimal_places=9, 
            blank=True, null=True, help_text="""Time in minutes to achieve the 
            desired step temperature – useful particularly for temperature mashes where 
            it may take some time to achieve the step temperature.""")
    end_temp = models.DecimalField(_("end temperature"), max_digits=14, decimal_places=9, 
            blank=True, null=True, help_text="""The temperature you can expect the mash to 
            fall to after a long mash step. Measured in degrees Celsius.""")
    
    # Optional extension for BeerXML display
    description = models.TextField(_("description"), blank=True, null=True, 
            help_text="""Textual description of this step such as 
            “Infuse 4.5 gal of water at 170 F” – may be either generated by 
            the program or input by the user.""")
    water_grain_ratio = models.CharField(_("water - grain ratio"), max_length=50, 
            blank=True, null=True, help_text="""The total ratio of water to grain 
            for this step AFTER the infusion along with the units, usually expressed 
            in qt/lb or l/kg. Note this value must be consistent with the required 
            infusion amount and amounts added in earlier steps and is only relevant as part 
            of a <MASH> profile. For example “1.5 qt/lb” or “3.0 l/kg”""")
    decoction_amt = models.CharField(_("decoction amount"), max_length=50, blank=True, 
            null=True, help_text="""Calculated volume of mash to decoct. Only applicable 
            for a decoction step. Includes the units as in “7.5 l” or “2.3 gal”""")
    infuse_temp = models.CharField(_("infuse temp"), max_length=50, blank=True, null=True,
            help_text="""The calculated infusion temperature based on the current step, grain, 
            and other settings. Applicable only for an infusion step. Includes the units as in 
            “154 F” or “68 C”""")
    display_step_temp = models.CharField(_("display step temperature"), max_length=50, 
            blank=True, null=True, help_text="""Step temperature in user defined 
            temperature units. For example “154F” or “68 C”""")
    display_infuse_amt = models.CharField(_("display infuse amount"), max_length=50, 
            blank=True, null=True, help_text="""Infusion amount along with the volume 
            units as in “20 l” or “13 qt”""")
    
    _beerxml_attrs = {
        "type": "mash_type",
        "decoction_amount": "decoction_amt"
    }

    def __unicode__(self):
        return u"%s" % self.name

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.mash_type:
            self.mash_type = u"%s" % self.mash_type.lower()
        

class MashProfile(BeerXMLBase):
    """
    A mash profile is a record used either within a recipe or 
    outside the recipe to precisely specify the mash method used. 
    The record consists of some informational items followed by a 
    <MASH_STEPS> record that contains the actual mash steps.
    """
    
    grain_temp = models.DecimalField(_("grain temperature"), max_digits=14, 
            decimal_places=9, help_text="""The temperature of the grain before 
            adding it to the mash in degrees Celsius.""")
    mash_steps = models.ManyToManyField(MashStep)
    notes = models.TextField(_("notes"), blank=True, null=True)
    tun_temp = models.DecimalField(_("tun temperature"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""Grain tun 
            temperature – may be used to adjust the infusion temperature for 
            equipment if the program supports it. Measured in degrees C.""")
    sparge_temp = models.DecimalField(_("sparge temperature"), max_digits=14, 
            decimal_places=9, blank=True, null=True, 
            help_text="Temperature of the sparge water used in degrees Celsius.")
    ph = models.DecimalField(_("sparge PH"), max_digits=14, decimal_places=9, 
            blank=True, null=True, help_text="PH of the sparge.")
    tun_weight = models.DecimalField(_("tun weight (kilos)"), max_digits=14, 
            decimal_places=9, blank=True, null=True, 
            help_text="Weight of the mash tun in kilograms")
    tun_specific_heat = models.DecimalField(_("tun specific heat"), max_digits=14, 
            decimal_places=9, blank=True, null=True, 
            help_text="Specific heat of the tun material in calories per gram-degree C.")
    equip_adjust = models.BooleanField(_("adjust from equipment"), default=False, 
            help_text="""If True, mash infusion and decoction calculations should take 
            into account the temperature effects of the equipment (tun specific heat and 
            tun weight). If False, the tun is assumed to be pre-heated. Default is False.""")
    
    # Optional extension for BeerXML display
    display_grain_temp = models.CharField(_("display grain temperature"), max_length=50, 
            blank=True, null=True, help_text="""Grain temperature in user display units 
            with the units. For example: “72 F”.""")
    display_tun_temp = models.CharField(_("display tun temperature"), max_length=50, 
            blank=True, null=True, help_text="""Tun temperature in user display units. 
            For example “68 F”""")
    display_sparge_temp = models.CharField(_("display sparge temperature"), max_length=50, 
            blank=True, null=True, help_text="""Sparge temperature in user defined units. 
            For example “178 F”""")
    display_tun_weight = models.CharField(_("display tun weight"), max_length=50, 
            blank=True, null=True, help_text="""Tun weight in user defined units 
            – for example “10 lb”""")
    
    def __unicode__(self):
        return u"%s" % self.name
    
    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)


class Misc(BeerXMLBase):
    """
    Database model for various items
    """
    
    TYPE = (
        (u"spice", u"Spice"),
        (u"fining", u"Fining"),
        (u"water agent", u"Water agent"),
        (u"herb", u"Herb"),
        (u"flavor", u"Flavor"),
        (u"other", u"Other")
    )
    
    USE = (
       (u"boil", u"Boil"),
       (u"mash", u"Mash"),
       (u"primary", u"Primary"),
       (u"secondary", u"Secondary"),
       (u"bottling", u"Bottling")
    )
    
    # NOTE: type is a reserved python word.
    misc_type = models.CharField(_("hop type"), max_length=12, choices=TYPE, default=4)
    use = models.CharField(_("hop type"), max_length=12, choices=USE, default=2)
    time = models.DecimalField(_("time"), max_digits=14, decimal_places=9,
            help_text="Amount of time the misc was boiled, steeped, mashed, etc in minutes.")
    amount = models.DecimalField(_("yield percentage"), max_digits=14, decimal_places=9,
            help_text="""Amount of item used. The default measurements are by weight, 
            but this may be the measurement in volume units if AMOUNT_IS_WEIGHT is set 
            to TRUE for this record. For liquid items this is liters, for solid the  
            weight is measured in kilograms.""")
    amount_is_weight = models.BooleanField(_("amount is weight"), default=False,
            help_text="""TRUE if the amount measurement is a weight measurement and FALSE if 
            the amount is a volume measurement.""")
    use_for = models.TextField(_("use for"), blank=True, null=True,
            help_text="Short description of what the ingredient is used for in text")
    notes = models.TextField(_("notes"), blank=True, null=True,
            help_text="Detailed notes on the item including usage.")
    
    # Optional extension for BeerXML display
    display_amount = models.CharField(_("display amount"), max_length=50, blank=True, 
            null=True, help_text="""The amount of the item in this record along with 
            the units formatted for easy display in the current user defined units. 
            For example “1.5 lbs” or “2.1 kg”.""")
    inventory = models.CharField(_("inventory"), max_length=50, blank=True, null=True,
            help_text="""Amount in inventory for this item along with the units 
            – for example “10.0 lb.”""")
    display_time = models.CharField(_("display time"), max_length=50, blank=True, 
            null=True, help_text="""Time in appropriate units along with the units 
            as in “10 min” or “3 days”.""")
    
    _beerxml_attrs = {
        "type": "misc_type"
    }
    
    def __unicode__(self):
        return u"%s" % self.name
    
    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.misc_type:
            self.misc_type = u"%s" % self.misc_type.lower()
        if self.use:
            self.use = u"%s" % self.use.lower()
    
    
class Yeast(BeerXMLBase):
    """
    Database model for yeast
    """
    
    TYPE = (
        (u"ale", u"Ale"),
        (u"lager", u"Lager"),
        (u"wheat", u"Wheat"),
        (u"wine", u"Wine"),
        (u"champagne", u"Champagne")
    )
    
    FORM = (
        (u"liquid", u"Liquid"),
        (u"dry", u"Dry"),
        (u"slant", u"Slant"),
        (u"culture", u"Culture")
    )
    
    FLOCCULATION = (
        (u"low", u"Low"),
        (u"medium", u"Medium"),
        (u"high", u"High"),
        (u"very high", u"Very high")
    )
    
    # NOTE: type is a reserved python word.
    yiest_type = models.CharField(_("yeast type"), max_length=12, choices=TYPE, 
                                  default=1)
    form = models.CharField(_("yeast form"), max_length=12, choices=FORM, default=1)
    amount = models.DecimalField(_("amount"), max_digits=14, decimal_places=9,
            help_text="""The amount of yeast, measured in liters. For a starter this is the 
            size of the starter. If the flag AMOUNT_IS_WEIGHT is set to TRUE then this 
            measurement is in kilograms and not liters.""")
    amount_is_weight = models.BooleanField(_("amount is weight or litres"), default=False,
            help_text="""TRUE if the amount measurement is a weight measurement and FALSE 
            if the amount is a volume measurement.  Default value (if not present) is 
            assumed to be FALSE – therefore the yeast measurement is a liquid amount 
            by default.""")
    laboratory = models.CharField(_("laboratory name"), max_length=100, blank=True, null=True)
    product_id = models.CharField(_("product id"), max_length=100, blank=True, null=True,
            help_text="""The manufacturer’s product ID label or number that identifies this 
            particular strain of yeast.""")
    min_temperature = models.DecimalField(_("min temperature"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""The minimum 
            recommended temperature for fermenting this yeast strain in degrees 
            Celsius.""")
    max_temperature = models.DecimalField(_("max temperature"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""The maximum 
            recommended temperature for fermenting this yeast strain in Celsius.""")
    flocculation = models.CharField(_("yeast form"), max_length=12, choices=FLOCCULATION, 
                                    default=1, blank=True, null=True)
    attenuation = models.DecimalField(_("attenuation percentage"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""Average 
            attenuation for this yeast strain.""")
    notes = models.TextField(_("notes"), blank=True, null=True)
    best_for = models.TextField(_("best for"), blank=True, null=True,
            help_text="Styles or types of beer this yeast strain is best suited for.")
    times_cultured = models.PositiveSmallIntegerField(_("times recultured"), 
            blank=True, null=True, help_text="""Number of times this yeast has 
            been reused as a harvested culture. This number should be zero if this 
            is a product directly from the manufacturer.""")
    max_reuse = models.PositiveSmallIntegerField(_("max recultures"), blank=True, 
            null=True, help_text="""Recommended of times this yeast can be reused 
            (recultured from a previous batch)""")
    add_to_secondary = models.BooleanField(_("amount is weight"), default=False,
            help_text="""Flag denoting that this yeast was added for a secondary (or later) 
            fermentation as opposed to the primary fermentation. Useful if one uses two              
            or more yeast strains for a single brew (eg: Lambic). Default value is FALSE.""")
    
    # Optional extension for BeerXML display
    display_amount = models.CharField(_("display amount"), max_length=50, blank=True, null=True,
            help_text="""The amount of yeast or starter in this record along with the units 
            formatted for easy display in the current user defined units. For example “1.5 oz” 
            or “100 g”.""")
    disp_min_temp = models.CharField(_("display minimum temperature"), max_length=50, blank=True,
            null=True, help_text="""Minimum fermentation temperature converted to current user 
            units along with the units. For example “54.0 F” or “24.2 C”""")
    disp_max_temp = models.CharField(_("display minimum temperature"), max_length=50, blank=True,
            null=True, help_text="""Maximum fermentation temperature converted to current 
            user units along with the units. For example “54.0 F” or “24.2 C”""")
    inventory = models.CharField(_("inventory"), max_length=50, blank=True, null=True,
            help_text="Amount in inventory for this hop along with the units – for example “10.0 pkgs”")
    culture_date = models.CharField(_("inventory"), max_length=50, blank=True, null=True,
            help_text="Date sample was last cultured in a neutral date form such as “10 Dec 04”")
    
    _beerxml_attrs = {
        "type": "yiest_type"
    }
    
    def __unicode__(self):
        return u"%s" % self.name

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.yiest_type:
            self.yiest_type = u"%s" % self.yiest_type.lower()
        if self.form:
            self.form = u"%s" % self.form.lower()
        if self.flocculation:
            self.flocculation = u"%s" % self.flocculation.lower()
    
    
class Water(BeerXMLBase):
    """
    Waters
    """
    amount = models.DecimalField(_("amount"), max_digits=14, decimal_places=9,
            help_text="Volume of water to use in a recipe in liters.")
    calcium = models.DecimalField(_("calcium"), max_digits=14, decimal_places=9,
            help_text="The amount of calcium (Ca) in parts per million.")
    bicarbonate = models.DecimalField(_("bicarbonate"), max_digits=14, decimal_places=9,
            help_text="The amount of bicarbonate (HCO3) in parts per million.")
    sulfate = models.DecimalField(_("sulfate"), max_digits=14, decimal_places=9, 
            help_text="The amount of Sulfate (SO4) in parts per million.")
    chloride = models.DecimalField(_("chloride"), max_digits=14, decimal_places=9,
            help_text="The amount of Chloride (Cl) in parts per million.")
    sodium = models.DecimalField(_("sodium"), max_digits=14, decimal_places=9,
            help_text="The amount of Sodium (Na) in parts per million.")
    magnesium = models.DecimalField(_("magnesium"), max_digits=14, decimal_places=9,
            help_text="The amount of Magnesium (Mg) in parts per million.")
    ph = models.DecimalField(_("PH"), max_digits=14, decimal_places=9, blank=True,
            null=True, help_text="The PH value of the water")
    notes = models.TextField(_("notes"), blank=True, null=True)
    
    # Optional extension for BeerXML display
    display_amount = models.CharField(_("display amount"), max_length=50, 
            blank=True, null=True, help_text="""The amount of water in this 
            record along with the units formatted for easy display in the 
            current user defined units. For example “5.0 gal” or “20.0 l”.""")
    
    def __unicode__(self):
        return u"%s" % self.name
    
    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)
    
    
class Style(BeerXMLBase):
    """
    Database model for brewing styles
    """
    
    TYPE = (
        (u"lager", u"Lager"),
        (u"ale", u"Ale"),
        (u"mead", u"Mead"),
        (u"wheat", u"Wheat"),
        (u"mixed", u"Mixed"),
        (u"cider", u"Cider")
    )
    
    category = models.CharField(_("category"), max_length=100, 
            help_text="""Category that this style belongs to – usually 
            associated with a group of styles such as  “English Ales” or 
            “Amercian Lagers”.""")
    category_number = models.CharField(_("category number"), max_length=10,
            help_text="""Number or identifier associated with this style category. 
            For example in the BJCP style guide, the “American Lager” category has 
            a category number of “1”.""")
    style_letter = models.CharField(_("style letter (uppercase)"), max_length=10,
            help_text="""The specific style number or subcategory letter associated 
            with this particular style. For example in the BJCP style guide, an 
            American Standard Lager would be style letter “A” under the main category. 
            Letters should be upper case.""")
    style_guide = models.CharField(_("style guide"), max_length=10, 
            help_text="""The name of the style guide that this particular style or 
            category belongs to. For example “BJCP” might denote the BJCP style guide, 
            and “AHA” would be used for the AHA style guide.""")
    # NOTE: type is a reserved python word.
    style_type = models.CharField(_("type"), max_length=12, choices=TYPE, default=1,
            help_text="""May be “Lager”, “Ale”, “Mead”, “Wheat”, “Mixed” or “Cider”. 
            Defines the type of beverage associated with this category.""")
    og_min = models.DecimalField(_("min OG"), max_digits=14, decimal_places=9, 
            help_text="""The minimum specific gravity as measured relative to water. 
            For example “1.040” might be a reasonable minimum for a Pale Ale.""")
    og_max = models.DecimalField(_("max OG"), max_digits=14, decimal_places=9,
            help_text="The maximum specific gravity as measured relative to water.")
    fg_min = models.DecimalField(_("min FG"), max_digits=14, decimal_places=9,
            help_text="The minimum final gravity as measured relative to water.")
    fg_max = models.DecimalField(_("max FG"), max_digits=14, decimal_places=9,
            help_text="The maximum final gravity as measured relative to water.")
    ibu_min = models.DecimalField(_("min IBU"), max_digits=14, decimal_places=9, 
            help_text="""The recommended minimum bitterness for this style as measured 
            in International Bitterness Units (IBUs)""")
    ibu_max = models.DecimalField(_("max IBU"), max_digits=14, decimal_places=9, 
            help_text="""The recommended maximum bitterness for this style as measured 
            in International Bitterness Units (IBUs)""")
    color_min = models.DecimalField(_("min color(SRM)"), max_digits=14, decimal_places=9,
            help_text="The minimum recommended color in SRM")
    color_max = models.DecimalField(_("max color(SRM)"), max_digits=14, decimal_places=9,
            help_text="The maximum recommended color in SRM.")
    abv_min = models.DecimalField(_("min ABV %"), max_digits=14, decimal_places=9, 
            blank=True, null=True, help_text="""The minimum recommended alcohol by 
            volume as a percentage.""")
    abv_max = models.DecimalField(_("max ABV %"), max_digits=14, decimal_places=9, 
            blank=True, null=True, help_text="""The maximum recommended alcohol by 
            volume as a percentage.""")
    carb_min = models.DecimalField(_("min carb (vols of CO2)"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""Minimum recommended 
            carbonation for this style in volumes of CO2""")
    carb_max = models.DecimalField(_("max carb (vols of CO2)"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""The maximum 
            recommended carbonation for this style in volumes of CO2""")
    notes = models.TextField(_("notes"), blank=True, null=True)
    profile = models.TextField(_("profile"), blank=True, null=True, 
                               help_text="Flavor and aroma profile for this style")
    ingredients = models.TextField(_("ingredients"), blank=True, null=True, 
                                   help_text="Suggested ingredients for this style")
    examples = models.TextField(_("examples"), blank=True, null=True, 
                                help_text="Example beers of this style.")
    
    # Optional extension for BeerXML display
    display_og_min = models.CharField(_("display OG minimum"), max_length=50, 
            blank=True, null=True, help_text="""Original gravity minimum in user 
            defined units such as “1.036 sg”""")
    display_og_max = models.CharField(_("display OG maximum"), max_length=50, 
            blank=True, null=True, help_text="""Original gravity max in user 
            defined units such as “1.056 sg”""")
    display_fg_min = models.CharField(_("display FG minimum"), max_length=50, 
            blank=True, null=True, help_text="""Final gravity minimum in user 
            defined units such as “1.010 sg”""")
    display_fg_max = models.CharField(_("display FG maximum"), max_length=50, 
            blank=True, null=True, help_text="""Final gravity maximum in user 
            defined units such as “1.019 sg”""")
    display_color_min = models.CharField(_("display color minimum"), max_length=50, 
            blank=True, null=True, help_text="""Minimum color in user defined units 
            such as “30 srm”""")
    display_color_max = models.CharField(_("display color maximum"), max_length=50, 
            blank=True, null=True, help_text="""Maximum color in user defined units 
            such as “20 srm”""")
    og_range = models.CharField(_("OG range"), max_length=50, blank=True, null=True,
            help_text="Original gravity range for the style such as “1.030-1.040 sg”")
    fg_range = models.CharField(_("FG range"), max_length=50, blank=True, null=True,
            help_text="Final gravity range such as “1.010-1.015 sg”")
    ibu_range = models.CharField(_("IBU range"), max_length=50, blank=True, null=True,
            help_text="Bitterness range in IBUs such as “10-20 IBU”")
    carb_range = models.CharField(_("carbonation range"), max_length=50, blank=True, 
            null=True, help_text="Carbonation range in volumes such as “2.0-2.6 vols”")
    color_range = models.CharField(_("color range"), max_length=50, blank=True, null=True,
            help_text="Color range such as “10-20 SRM”")
    abv_range = models.CharField(_("ABV range"), max_length=50, blank=True, null=True,
            help_text="ABV Range for this style such as “4.5-5.5%”")
    
    _beerxml_attrs = {
        "type": "style_type"
    }
    
    def __unicode__(self):
        return u"%s" % self.name

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.style_type:
            self.style_type = u"%s" % self.style_type.lower()
    
    
class Recipe(BeerXMLBase):
    """
    Database model for reciepes
    """
    TYPE = (
        (u"extract", u"Extract"),
        (u"partial mash", u"Partial Mash"),
        (u"all grain", u"All grain")
    )
    
    IBU_METHOD = (
        (u"rager", u"Rager"),
        (u"tinseth", u"Tinseth"),
        (u"garetz", u"Garetz")
    )
    
    recipe_type = models.CharField(_("type"), max_length=12, choices=TYPE)
    # NOTE: Even though Style is a required beerxml field, we set this as
    # null=True, to solve a recursive dependency problem in the 
    # BeerXMLNode.get_or_create() method.
    style = models.ForeignKey(Style, null=True, help_text="""The style of the 
            beer this recipe is associated with.""")
    equipment = models.ForeignKey(Equipment, blank=True, null=True, 
            help_text="""An equipment record is optional. If included the 
            Batch size and Boil size in the equipment record must match 
            the values in this recipe record.""")
    brewer = models.CharField(_("name of brewer"), max_length=100)
    asst_brewer = models.CharField(_("assistant brewer"), max_length=100, blank=True, 
                                   null=True)
    batch_size = models.DecimalField(_("batch size"), max_digits=14, decimal_places=9,
            help_text="Target size of the finished batch in liters.")
    boil_size = models.DecimalField(_("boil size"), max_digits=14, decimal_places=9,
            help_text="Starting size for the main boil of the wort in liters.")
    boil_time = models.DecimalField(_("boil time"), max_digits=14, decimal_places=9,
            help_text="The total time to boil the wort in minutes.")
    efficiency = models.DecimalField(_("efficiency"), max_digits=14, decimal_places=9, 
            blank=True, null=True, help_text="""The percent brewhouse efficiency to be 
            used for estimating the starting gravity of the beer. Not required for 
            “Extract” recipes, but is required for “Partial Mash” and “All Grain” recipes.""")
    hops = models.ManyToManyField(Hop, blank=True, null=True, 
                                  help_text="Zero or more hop ingredients")
    fermentables = models.ManyToManyField(Fermentable, blank=True, null=True, 
                                          help_text="Zero or more fermentable ingredients")
    miscs = models.ManyToManyField(Misc, blank=True, null=True, 
                                   help_text="Zero or more misc records")
    yeasts = models.ManyToManyField(Yeast, blank=True, null=True, 
                                    help_text="Zero or more yeast records")
    waters = models.ManyToManyField(Water, blank=True, null=True, 
                                    help_text="Zero or more water records")
    mash = models.ForeignKey(MashProfile, blank=True, null=True, 
            help_text="""A MASH profile record containing one or more Mash steps. 
            NOTE: No Mash record is needed for “Extract” type brews.""")
    notes = models.TextField(_("notes"), blank=True, null=True)
    taste_notes = models.TextField(_("taste notes"), blank=True, null=True)
    taste_rating = models.DecimalField(_("taste rating BJCP"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""Number between 
            zero and 50.0 denoting the taste rating – corresponds to the 50 point
             BJCP rating system.""")
    og = models.DecimalField(_("OG"), max_digits=14, decimal_places=9, blank=True, 
            null=True, help_text="""The measured original (pre-fermentation) 
            specific gravity of the beer.""")
    fg = models.DecimalField(_("FG"), max_digits=14, decimal_places=9, blank=True, 
            null=True, help_text="The measured final gravity of the finished beer.")
    fermentation_stages = models.PositiveSmallIntegerField(_("fermentation stages"), 
            blank=True, null=True, help_text="""The number of fermentation stages 
            used – typically a number between one and three""")
    primary_age = models.DecimalField(_("primary age (days)"), max_digits=14, 
            decimal_places=9, blank=True, null=True, 
            help_text="Time spent in the primary in days")
    primary_temp = models.DecimalField(_("primary temperature (Celsius)"), 
            max_digits=14, decimal_places=9, blank=True, null=True, 
            help_text="Temperature in degrees Celsius for the primary fermentation")
    secondary_age = models.DecimalField(_("secondary age (days)"), max_digits=14, 
            decimal_places=9, blank=True, null=True, 
            help_text="Time spent in the secondary in days")
    secondary_temp = models.DecimalField(_("secondary temperature (Celsius)"), 
            max_digits=14, decimal_places=9, blank=True, null=True, 
            help_text="Temperature in degrees Celsius for the secondary fermentation")
    tertiary_age = models.DecimalField(_("tertiary age (days)"), max_digits=14, 
            decimal_places=9, blank=True, null=True, 
            help_text="Time spent in the third fermenter in days")
    tertiary_temp = models.DecimalField(_("tertiary temperature (Celsius)"), 
            max_digits=14, decimal_places=9, blank=True, null=True, 
            help_text="Temperature in the tertiary fermenter")
    age = models.DecimalField(_("age"), max_digits=14, decimal_places=9, blank=True, 
            null=True, help_text="The time to age the beer in days after bottling")
    age_temp = models.DecimalField(_("age temperature"), max_digits=14, decimal_places=9, 
            blank=True, null=True, help_text="Temperature for aging the beer after bottling")
    date = models.CharField(_("date"), max_length=50, blank=True, null=True,
            help_text="Brew date in a easily recognizable format such as “3 Dec 04”.")
    real_date = models.DateField(_("real date"), blank=True, null=True, 
            help_text="Brew date in a computer-readable format")
    carbonation = models.DecimalField(_("carbonation"), max_digits=14, decimal_places=9, 
            blank=True, null=True, help_text="""Floating point value corresponding to the 
            target volumes of CO2 used to carbonate this beer""")
    forced_carbonation = models.BooleanField(_("forced carbonation"), default=False, 
            help_text="""True if the batch was force carbonated using CO2 pressure, False if 
            the batch was carbonated using a priming agent""")
    priming_sugar_name = models.CharField(_("priming sugar name"), max_length=50, blank=True, 
            null=True, help_text="""Text describing the priming agent such as “Honey” or 
            “Corn Sugar” – used only if this is _not_ a forced carbonation""")
    carbonation_temp = models.DecimalField(_("carbonation temperature (Celsius)"), max_digits=14, 
            decimal_places=9, blank=True, null=True, 
            help_text="The temperature for either bottling or forced carbonation")
    priming_sugar_equiv = models.DecimalField(_("priming sugar equivalent"), max_digits=14,
            decimal_places=9, blank=True, null=True, help_text="""Factor used to 
            convert this priming agent to an equivalent amount of corn sugar 
            for a bottled scenario. For example, “Dry Malt Extract” would have 
            a value of 1.4 because it requires 1.4 times as much DME as corn sugar 
            to carbonate. To calculate the amount of DME needed, the program can 
            calculate the amount of corn sugar needed and then multiply by this factor.""")
    keg_priming_factor = models.DecimalField(_("keg priming factor"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""Used to factor in 
            the smaller amount of sugar needed for large containers. For example, 
            this might be 0.5 for a typical 5 gallon keg since naturally priming a 
            keg requires about 50% as much sugar as priming bottles""")
    
    # Optional extension for BeerXML display
    est_og = models.CharField(_("estimated OG"), max_length=50, blank=True, 
            null=True, help_text="""Calculated estimate of the original 
            gravity for this recipe along with the units""")
    est_fg = models.CharField(_("estimated FG"), max_length=50, blank=True, 
            null=True, help_text="""Calculated estimate for the final specific 
            gravity of this recipe along with the units as in “1.015 sg”""")
    est_color = models.CharField(_("estimated color"), max_length=50, blank=True, 
            null=True, help_text="The estimated color of the beer in user defined color units")
    ibu = models.DecimalField(_("IBU"), max_digits=14, decimal_places=9, blank=True, 
            null=True, help_text="The estimated bitterness level of the beer in IBUs")
    ibu_method = models.CharField(_("IBU method"), max_length=12, choices=IBU_METHOD, 
            blank=True, null=True, help_text="""May be “Rager”, “Tinseth” or “Garetz” 
            corresponding to the method/equation used to estimate IBUs for this recipe""")
    est_abv = models.DecimalField(_("estimated ABV"), max_digits=14, decimal_places=9, 
            blank=True, null=True, help_text="Estimated percent alcohol by volume for this recipe")
    abv = models.DecimalField(_("ABV"), max_digits=14, decimal_places=9, blank=True, null=True,
            help_text="Actual alcohol by volume calculated from the OG and FG measured")
    actual_efficiency = models.DecimalField(_("actual efficiency"), max_digits=14, 
            decimal_places=9, blank=True, null=True, 
            help_text="The actual efficiency as calculated using the measured original and final gravity")
    calories = models.CharField(_("calories"), max_length=50, blank=True, null=True,
            help_text="""Calorie estimate based on the measured starting and ending gravity. 
            Note that calories should be quoted in “Cal” or kilocalories which is the normal 
            dietary measure (i.e. a beer is usually in the range of 100-250 calories per 12 oz). 
            Examples “180 Cal/pint”""")
    display_batch_size = models.CharField(_("display batch size"), max_length=50, 
            blank=True, null=True, help_text="""Batch size in user defined units 
            along with the units as in “5.0 gal”""")
    display_boil_size = models.CharField(_("display boil size"), max_length=50, 
            blank=True, null=True, help_text="""Boil size with user defined 
            units as in “6.3 gal”""")
    display_og = models.CharField(_("display OG"), max_length=50, blank=True, 
            null=True, help_text="""Measured original gravity in user defined 
            units as in “6.4 plato”""")
    display_fg = models.CharField(_("display FG"), max_length=50, blank=True, 
            null=True, help_text="""Measured final gravity in user defined 
            units as in “1.035 sg”""")
    display_primary_temp = models.CharField(_("display primary temperature"), 
            max_length=50, blank=True, null=True, help_text="""Primary fermentation 
            temperature in user defined units such as “64 F”""")
    display_secondary_temp = models.CharField(_("display secondary temperature"), 
            max_length=50, blank=True, null=True, help_text="""Secondary fermentation 
            temperature in user defined units such as “56 F”""")
    display_tertiary_temp = models.CharField(_("display tertiary temperature"), 
            max_length=50, blank=True, null=True, help_text="""Tertiary temperature 
            in user defined units such as “20 C”""")
    display_age_temp = models.CharField(_("display age temperature"), max_length=50, 
            blank=True, null=True, help_text="""Temperature to use when aging the 
            beer in user units such as “55 F”""")
    carbonation_used = models.CharField(_("carbonation used"), max_length=50, 
            blank=True, null=True, help_text="""Text description of the carbonation 
            used such as “50g corn sugar” or “Kegged at 20psi”""")
    display_carb_temp = models.CharField(_("display carbonation temperature"), 
            max_length=50, blank=True, null=True, help_text="""Carbonation/Bottling 
            temperature in appropriate units such as “40F” or “32C”""")
    
    _beerxml_attrs = {
        "type": "recipe_type"
    }
    
    def __unicode__(self):
        return u"%s" % self.name

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.recipe_type:
            self.recipe_type = u"%s" % self.recipe_type.lower()
        if self.ibu_method:
            self.ibu_method = u"%s" % self.ibu_method.lower()
    
    

class RecipeOption(models.Model):
    """
    Each recipe can have a different set of options.
    """
    
    class Meta:
        app_label = "brewery"
        
    # Units
    WEIGHT = (
        (0, u"Use SI units"),
        (1, u"Use US traditional units"),
        (2, u"Use British imperial units")
    )
    
    VOLUME = (
        (0, u"Use SI units"),
        (1, u"Use US traditional units"),
        (2, u"Use British imperial units")
    )

    TEMPERATURE = (
        (0, u"Celsius"),
        (1, u"Fahrenheit")
    )

    GRAVITY = (
        (0, u"20C/20C Specific gravity"),
        (1, u"Plato/Brix/Bailing")
    )
    
    COLOR = (
        (0, u"Use SRM"),
        (1, u"Use EBC")
    )
    
    # Formulas
    COLOR_FORMULAS = (
        (0, u"Mosher's approximation"),
        (1, u"Daniel's approximation"),
        (2, u"Morey's approximation")
    )
    
    IBU_FORMULA = (
        (0, u"Tinseth's approximation"),
        (1, u"Rager's approximation"),
        (2, u"Garetz' approximation")
    )
    
    recipe = models.OneToOneField(Recipe)
    weight = models.PositiveSmallIntegerField(_("weight units"), choices=WEIGHT,
            default=1, help_text="Weight units for this recipe")
    volume = models.PositiveSmallIntegerField(_("volume units"), choices=VOLUME, 
            default=1, help_text="Volume units for this recipe")
    temperature = models.PositiveSmallIntegerField(_("temperature units"), 
            choices=TEMPERATURE, default=1, help_text="""Temperature units for 
            this recipe""")
    gravity = models.PositiveSmallIntegerField(_("gravity units"), 
            choices=GRAVITY, default=0, help_text="Gravity units for this recipe")
    color = models.PositiveSmallIntegerField(_("color system"), choices=COLOR, 
            default=0, help_text="Color system for this recipe")
    color_formula = models.PositiveSmallIntegerField(_("color formula"), 
            choices=COLOR_FORMULAS, default=2, help_text="""Color formula to use 
            for calculating the color for this recipe""")
    ibu_formula = models.PositiveSmallIntegerField(_("ibu formula"), choices=IBU_FORMULA, 
            default=0, help_text="IBU formula to use for calculating IBU for this recipe")
    slug = models.SlugField(max_length=100, blank=True)
    registered_by = models.ForeignKey(User, blank=True, null=True,
            related_name="%(app_label)s_%(class)s_registered_by_set", help_text="Registered by")
    modified_by = models.ForeignKey(User, blank=True, null=True,
            related_name="%(app_label)s_%(class)s_modified_by_set", help_text="Modified by")
    cdt = models.DateTimeField(_("created"), editable=False, auto_now_add=True)
    mdt = models.DateTimeField(_("modified"), editable=False, auto_now=True)
    
    def __unicode__(self):
        return u"%s Recipe options" % self.recipe.name
    
    def clean(self):
        if not self.slug:
            self.slug = slugify("%s-recipe-options" % self.recipe)


#
# Signals
#
# Brewery models depend on model cleaning to
# translate some BeerXML values to brewery compatible
# values. We need to hook onto the pre_save signal on
# each model to achieve that.
# NOTE: This is not very DRY, can it be done better?

@receiver(signals.pre_save, sender=Equipment)
def clean_equipment_callback(sender, instance, **kwargs):
    instance.clean()

@receiver(signals.pre_save, sender=Fermentable)
def clean_fermentable_callback(sender, instance, **kwargs):
    instance.clean()
    
@receiver(signals.pre_save, sender=Hop)
def clean_hop_callback(sender, instance, **kwargs):
    instance.clean()
    
@receiver(signals.pre_save, sender=MashStep)
def clean_mash_step_callback(sender, instance, **kwargs):
    instance.clean()
    
@receiver(signals.pre_save, sender=MashProfile)
def clean_mash_profile_callback(sender, instance, **kwargs):
    instance.clean()
    
@receiver(signals.pre_save, sender=Misc)
def clean_misc_callback(sender, instance, **kwargs):
    instance.clean()
    
@receiver(signals.pre_save, sender=Yeast)
def clean_yeast_callback(sender, instance, **kwargs):
    instance.clean()
    
@receiver(signals.pre_save, sender=Water)
def clean_water_callback(sender, instance, **kwargs):
    instance.clean()
    
@receiver(signals.pre_save, sender=Style)
def clean_style_callback(sender, instance, **kwargs):
    instance.clean()

@receiver(signals.pre_save, sender=Recipe)
def clean_recipe_callback(sender, instance, **kwargs):
    instance.clean()
    
@receiver(signals.pre_save, sender=RecipeOption)
def clean_recipe_option_callback(sender, instance, **kwargs):
    instance.clean()
    