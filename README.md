Brewery

This is a portable django-app for dealing with BeerXML brewing files.
It's currently in early alfa development, and should _not_ be used for
anything!

Currently implemented features are:
 * Complete BeerXML v1 models
 * Parse BeerXML files to:
  * A tuple of tuples
  * A list of dictionaries
  * A list of BeerXMLNodes, which is a class representing any BeerXML Element like Mash, Recipe, Hop, etc
 * Save BeerXML files directly to database, including nested children


Please see [Wiki](https://github.com/rhblind/brewery/wiki) for code examples