from lxml import etree
from brewery.beerxml.error import BeerXMLError
from brewery.beerxml.nodes import BeerXMLNode

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO    

def export_toxml(model_instance):
    """
    Export model instance to beerxml XML format
    """
    raise NotImplementedError("This feature is not yet implemented")

def export_tocsv(model_instance):
    """
    Export model instance to CSV format
    """
    raise NotImplementedError("This feature is not yet implemented")

def to_tuple(xmldata):
    """
    Reads a file or string to a tuple
    structure of the xml input data.
    """
    try:
        xml = StringIO(xmldata)
    except:
        if not isinstance(xmldata, file):
            raise BeerXMLError("Input data must be a file or str object")
        xml = StringIO(xmldata.read())
    
    tree = etree.parse(xml)

    parse_node = lambda node: \
        (node.tag, tuple(map(parse_node, node)) or node.text)

    root = tree.getroot()
    nodetree = parse_node(root)
    return nodetree

def to_dict(xmldata):
    """
    Reads a file or string to a dictionary
    structure of the xml input data.
    """
    try:
        xml = StringIO(xmldata)
    except:
        if not isinstance(xmldata, file):
            raise BeerXMLError("Input data must be a file or str object")
        xml = StringIO(xmldata.read())
    
    def listify(node):
        return node.tag, list(map(dictify, node)) or node.text
        
    def dictify(node):
        return node.tag, dict(map(dictify, node)) or node.text
    
    def keys(nodes):
        return dict([(n.getparent().tag, []) for n in nodes])
    
    children = etree.XPath("child::*[*]")
    attrs = etree.XPath("child::*[not(child::*)]")
    
    tree = etree.parse(xml)
    root = tree.getroot()
    nodes = children(root)
    
    nodetree = keys(nodes)
    for node in nodes:
        key = node.getparent().tag
        name, values = listify(node)
        node_dict = dict(map(iter, values))
        to_parse = [elem for elem in children(node) if children(elem)]
        
        for n in to_parse:
            node_attrs = [listify(attr) for attr in attrs(n)]
            if node_attrs:
                node_attrs = dict(map(iter, node_attrs))
                for child in children(n):
                    if not child.tag in node_attrs.keys():
                        node_attrs[child.tag] = []
                    for cc in map(dictify, child):
                        node_attrs[child.tag].append(dict([cc]))
            else:
                for cc in map(dictify, n):
                    node_attrs.append(dict([cc]))
            node_dict[n.tag] = node_attrs
        nodetree[key].append({name: node_dict})
    return nodetree

def to_beerxml(xmldata):
    """
    Reads a file or string to a dictionary
    structure of the xml input data with each
    node as a BeerXMLNode()
    """
    nodetree = to_dict(xmldata)
    for collection, items in nodetree.iteritems():
        nodetree[collection] = []
        while items:
            item_data = items.pop()
            for name, data in item_data.iteritems():
                node = BeerXMLNode(name=name, attrs=data)
                nodetree[collection].append(node)
    return nodetree
