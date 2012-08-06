# -*- coding: utf-8 -*-

from django.contrib import admin

from models import Equipment
from models import Fermentable
from models import Hop
from models import MashStep
from models import MashProfile
from models import Misc
from models import Yeast
from models import Water
from models import Style
from models import Recipe
from models import RecipeOption

class EquipmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class FermentableAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class HopAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class MashStepAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class MashProfileAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class MiscAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class YeastAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class WaterAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class StyleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class RecipeOptionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Fermentable, FermentableAdmin)
admin.site.register(Hop, HopAdmin)
admin.site.register(MashStep, MashStepAdmin)
admin.site.register(MashProfile, MashProfileAdmin)
admin.site.register(Misc, MiscAdmin)
admin.site.register(Yeast, YeastAdmin)
admin.site.register(Water, WaterAdmin)
admin.site.register(Style, StyleAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeOption, RecipeOptionAdmin)