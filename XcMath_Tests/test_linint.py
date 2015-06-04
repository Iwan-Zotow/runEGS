# -*- coding: utf-8 -*-

import unittest
import math

import linint
import point2d

class TestLinInt(unittest.TestCase):
    """
    Unit tests to check linear interpolator
    """

    @staticmethod
    def make_curve():
        """
        make test curve
        """
        curve = []
        curve.append(point2d.point2d(5.0, 1.0))
        curve.append(point2d.point2d(4.0, 2.0))
        curve.append(point2d.point2d(3.0, 3.0))
        curve.append(point2d.point2d(2.0, 4.0))
        curve.append(point2d.point2d(1.0, 5.0))
        
        return curve
    
    def test_constructor(self):
        """
        test linint construction
        """
        
        li = linint.linint(TestLinInt.make_curve())
        
        self.assertTrue(len(li) == 5)
        
    def test_interpolation(self):
        """
        test interpolation
        """
        
        li = linint.linint(TestLinInt.make_curve())
        v  = li.interpolate(4.5)
                
        self.assertTrue(math.fabs(v - 1.5) < 0.001)
        

if __name__ == '__main__':
    unittest.main()
