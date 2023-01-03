   
import unittest
import sys
import os
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "../")) 
import pygame_gui_xml.xmlparser as xmlparser
   
# Coming Soon once the library is more mature
class XMLParserTest(unittest.TestCase):
    def test_mainmenu_example(self):
        try:
            xmlparser.parse_pygame_xml( os.path.join( os.path.dirname(os.path.abspath(__file__)), "data/mainmenu.xml" ))
            self.assertTrue(True)
        except Exception as exep:
            self.fail(str(exep))
        
if __name__ == "__main__":
    unittest.main()