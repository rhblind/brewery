# -*- coding: utf-8 -*-

from error import BeerXMLError, BeerXMLValidationError

from django.db.models.loading import get_model
from django.utils.encoding import smart_str
from django.db.models.fields import FieldDoesNotExist
from django.db.models.fields.related import ManyToOneRel, ManyToManyRel
from django.core.exceptions import ValidationError

# Mapping of BeerXML standard node tags to brewery models
NODENAMES = {
    "EQUIPMENT"   : "Equipment",
    "FERMENTABLE" : "Fermentable",
    "HOP"         : "Hop",
    "MASH"        : "MashProfile",
    "MASH_STEP"   : "MashStep",
    "MISC"        : "Misc",
    "YEAST"       : "Yeast",
    "WATER"       : "Water",
    "STYLE"       : "Style",
    "RECIPE"      : "Recipe"
}

class BeerXMLNode(dict):
    """
    This class is used to map an xml node
    to a brewery model.
    
    """
    def __init__(self, name, attrs):
        """
        Convert values to correct python data type,
        and update naming conventions.
        
        If model has some naming conventions which differs from
        XML element tags, these should be listed in the _beerxml_attrs
        dictionary attribute of the model.
        This method compare the element to the model attributes and
        sets the name which should be used.
        """
        
        super(BeerXMLNode, self).__init__()
        assert isinstance(attrs, dict), \
            "attrs must be a dict of attributes"
        
        self.__name__ = name
        defaults = attrs.copy()
        for key, value in defaults.iteritems():
            # Switch names with model attribute names
            model_name = key = key.lower()
            if hasattr(self._model, "_beerxml_attrs"):
                key = self._model._beerxml_attrs.get(model_name, key)
            
            # Update boolean field names to a value
            # to_python() can deal with
            if value in ("TRUE", "FALSE"):
                if value == "TRUE":
                    value = "True"
                else:
                    value = "False"
            
            try:
                field = self._model._meta.get_field(key)
                value = field.to_python(value)
                if isinstance(field.rel, ManyToOneRel):
                    value = BeerXMLNode(field.name.upper(), value)
                if isinstance(field.rel, ManyToManyRel):
                    values = []
                    if value:
                        for node in value:
                            for k, v in node.iteritems():
                                values.append(BeerXMLNode(k, v))
                    value = values
                self.update({key: value})   # update dict
                setattr(self, key, value)   # set as attribute
            except FieldDoesNotExist:
                # If field not does not exist on model,
                # continue to next
                continue
            except ValidationError, e:
                raise BeerXMLValidationError(e)
            except Exception, e:
                raise BeerXMLError(e)
    
    def __repr__(self):
        try:
            u = unicode(self.__name__)
        except (UnicodeEncodeError, UnicodeDecodeError):
            u = '[Bad Unicode data]'
        return smart_str(u'<%s: %s>' % (self.__class__.__name__, u))
    
    def _get_node_model(self):
        """
        Return the corresponding model for node
        """
        model = get_model("brewery", NODENAMES[self.__name__]) or None
        if model is None:
            raise BeerXMLValidationError("Could not find model: %s" % self.__name__) 
        return model
    _model = property(_get_node_model)
    
    def save(self):
        """
        Save this node and all dependent
        nodes to the database
        """
        pass

        