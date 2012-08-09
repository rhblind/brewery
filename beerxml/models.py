# -*- coding: utf-8 -*-

from error import BeerXMLError, BeerXMLValidationError

from django.utils.encoding import smart_str
from django.db.models.base import Model
from django.db.models.loading import get_model
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
        
        self.__name__ = name.upper()    # Always use upper case naming
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
                    value = BeerXMLNode(field.name, value)
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
        
        # Cache up related fields to save some iterations on save
        self.many_to_many = list(self.iter_field_type(ManyToManyRel))
        self.many_to_one = list(self.iter_field_type(ManyToOneRel))
    
    def __repr__(self):
        # Shamelessly copied from django
        try:
            u = unicode(self.__name__)
        except (UnicodeEncodeError, UnicodeDecodeError):
            u = "[Bad Unicode data]"
        return smart_str(u"<%s: %s>" % (self.__class__.__name__, u))
    
    def _get_node_model(self):
        """
        Return the corresponding model for node
        """
        model = get_model("brewery", NODENAMES[self.__name__]) or None
        if model is None:
            raise BeerXMLValidationError("Could not find model: %s" % self.__name__) 
        return model
    _model = property(_get_node_model)
    
    def iter_field_type(self, field_type):
        """
        Iterates over a node, yielding all fields
        which match field_type in a key, value paired
        dict.
        """
        for key in self.iterkeys():
            field = self._model._meta.get_field(key)
            if isinstance(field.rel, field_type):
                yield {key: self.get(field.name)}
    
    def get_or_create(self, **kwargs):
        """
        Save this node and all dependent
        nodes to the database
        """
        def get_clean_lookup(node):
            """
            Create a copy of this node without relations and
            __fields__. This "should" be able to save to model
            TODO: make pretty =)
            """
            lookup = dict([(k, v) for k, v in node.iteritems() if not "__" in k
                           and not (any(k in x.keys() for x in node.many_to_one) 
                                    or any(k in x.keys() for x in node.many_to_many))])
            return lookup
        
        def save_node_relations(node, obj, **kwargs):
            """
            node = BeerXMLNode(), obj = saved Model() instance.
            kwargs take a special dictionary called 'inherit',
            which can be used to set same attribute on all nodes.
            This is mainly used to set user attribute to same user
            when traversing the tree.
            
            Traverse the current node, looking for many-to-one and 
            many-to-many relations. If found, each relation is instantiated 
            and saved, then this method is called recursive until all 
            related nodes has been saved.
            """
            assert isinstance(node, BeerXMLNode), \
                "%s must be a BeerXMLNode instance." % node
                
            if isinstance(obj, Model):
                if not obj.pk:
                    raise BeerXMLError("%s must be a saved instance." % obj.__class__)
            else:
                raise BeerXMLError("%s must be a Model instance." % obj)
            
            inherit = kwargs.pop("inherit", {})
            try:
                # TODO: use get_or_create()
                # Add many-to-one (ForeignKey) relations
                for m2one in node.many_to_one:
                    for field_name, n in m2one.iteritems():
                        lookup = get_clean_lookup(n)
                        lookup.update(inherit)
                        rel_obj, created = n._model.objects.get_or_create(**lookup)
                        setattr(obj, field_name, rel_obj)
                        save_node_relations(n, rel_obj)
                
                # Add many-to-many relations
                for m2m in node.many_to_many:
                    for field_name, n_list in m2m.iteritems():
                        for n in n_list:
                            lookup = get_clean_lookup(n)
                            lookup.update(inherit)
                            rel_obj, created = n._model.objects.get_or_create(**lookup)
                            # Ugly hack to add many-to-many relations
                            # on arbitrary fields
                            m2m_field = obj.__getattribute__(field_name)
                            m2m_field.add(rel_obj)
                            save_node_relations(n, rel_obj)
            except Exception, e:
                raise BeerXMLError(e)
            
        try:
            lookup = get_clean_lookup(self)
            # update lookup with special inherit dict
            inherit = kwargs.pop("inherit", {})
            lookup.update(inherit)
            obj, created = self._model.objects.get_or_create(**lookup)
            save_node_relations(self, obj, inherit=inherit)
        except Exception, e:
            raise BeerXMLError(e)
        
        return obj, created
