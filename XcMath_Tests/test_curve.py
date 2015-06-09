# -*- coding: utf-8 -*-

import unittest
import os
import curve
import clinical

class TestCupCurve(unittest.TestCase):
    """
    Unit tests to check cup curve class
    """
    
    @staticmethod
    def make_cup_name(radUnit, outerCup, innerCupSer, innerCupNum):
        """
        Makes cup name out of unit, inner cup, outer cup series and number
        """
        return clinical.make_cup_name(radUnit, outerCup, innerCupSer, innerCupNum)        
        
    def test_constructor(self):
        """
        Constructor test 1
        """
        cupdir = "cup_geometry"     
        radUnit  = "8"
        outerCup = "2"
        innerCupSer = "M"
        innerCupNum = "01"
    
        fname  = TestCupCurve.make_cup_name(radUnit, outerCup, innerCupSer, innerCupNum)
        fname += "_" + "KddCurveA.txt"
        filename = os.path.join("..", cupdir, fname)
    
        cup = curve.curve(filename)
        
        self.assertTrue(cup.curve() != None)

if __name__ == '__main__':
    unittest.main()
