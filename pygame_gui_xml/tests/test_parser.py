   
import unittest
import pygame_gui_xml.parser as xmlparser
   
class XMLParserTest(unittest.TestCase):
    def test_mainmenu_example(self):
        try:
            xmlparser.parse_pygame_xml("pggxml/tests/data/mainmenu.xml")
            self.assertTrue(True)
        except Exception as exep:
            self.fail(str(exep))
        
if __name__ == "__main__":
    unittest.main()