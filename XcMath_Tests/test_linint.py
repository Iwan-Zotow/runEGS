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
        
    def test_interpolation2(self):
        """
        test interpolation 2
        """
        
        li = linint.linint(TestLinInt.make_curve())
        v  = li.interpolate(4.7)
                
        self.assertTrue(math.fabs(v - 1.3) < 0.001)

    def test_interpolation3(self):
        """
        test interpolation 3
        """
        
        li = linint.linint(TestLinInt.make_curve())
        v  = li.interpolate(2.8)
                
        self.assertTrue(math.fabs(v - 3.2) < 0.001)

    def test_extrapolation1(self):
        """
        test extrapolation 1
        """
        
        li = linint.linint(TestLinInt.make_curve())
        v  = li.extrapolate(5.01)
                
        self.assertTrue(math.fabs(v - 0.0) < 0.001)

    def test_extrapolation2(self):
        """
        test extrapolation 2
        """
        
        li = linint.linint(TestLinInt.make_curve())
        v  = li.extrapolate(0.9)
                
        self.assertTrue(math.fabs(v - 5.1) < 0.001)

    def test_extrapolation3(self):
        """
        test extrapolation 2
        """
        
        li = linint.linint(TestLinInt.make_curve())
        v  = li.extrapolate(0.2)
                
        self.assertTrue(math.fabs(v - 5.8) < 0.001)

if __name__ == '__main__':
    unittest.main()
