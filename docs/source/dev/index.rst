.. _dev:

Internals
================

| This "Internals" section is not meant for any specific reason but to explain **how** the library works, in case a contributor wants to quickly get up to speed or for anyone that is simply curious
| In essence, the pygame_gui_xml library works in 4 steps
| First, the library takes xml data and parses it with Beautiful Soup 4 library (shoutout bs4). 
| Next, the library takes that XML data and parses the attributes and 

- As of now, The ast.py module defines a general API to construct an XML Schema with different values and requirements that can be parsed into an XML Node Tree
- The parser.py module defines the actual specific schema of pygame_gui_xml and parses the XML into the XML Tree Node
- The XML is then turned into a GUI Tree where the values for each of the XML Nodes can be stored into a specific format
- Lastly, the GUI Tree is used by a GUI object to create and update the pygame gui for the end user

================

.. toctree::
    :maxdepth: 4

    ast
    parser
    guitree
    gui
