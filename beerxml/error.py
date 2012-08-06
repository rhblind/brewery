# -*- coding: utf-8 -*-

class BeerXMLError(Exception):
    """
    This class is just for convention, so
    that we can raise cool BeerXML errors
    (no pun intended)
    """
    pass


class BeerXMLValidationError(BeerXMLError):
    pass
