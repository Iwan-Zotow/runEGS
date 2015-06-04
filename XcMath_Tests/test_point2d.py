# -*- coding: utf-8 -*-

import unittest
from os import path
import curve

class TestCupCurve(unittest.TestCase):
    """
    Unit tests to check cup curve class
    """
    
    @staticmethod
    def make_cup_name(radUnit, outerCup, innerCupSer, innerCupNum):
        """
        """
        return "R" + radUnit + "O" + outerCup + "I" + innerCupSer + innerCupNum
    
    def test_constructor(self):
        cupdir = "cup_geometry"     
        radUnit  = "8"
        outerCup = "2"
        innerCupSer = "M"
        innerCupNum = "01"
    
        fname  = TestCupCurve.make_cup_name(radUnit, outerCup, innerCupSer, innerCupNum)
        fname += "_" + "KddCurveA.txt"
        filename = path.join("..", cupdir, fname)
    
        cup = curve.curve(filename)
        
        self.assertTrue(cup.curve() != None)

if __name__ == '__main__':
    unittest.main()
