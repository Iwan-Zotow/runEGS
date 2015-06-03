# -*- coding: utf-8 -*-

import numpy as np
import unittest

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
        test passable cm2mm conversion
        """
        
        li = linint.linint(TestLinInt.make_curve())
        
        self.assertTrue(len(li) == 5)

if __name__ == '__main__':
    unittest.main()
