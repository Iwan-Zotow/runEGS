# -*- coding: utf-8 -*-

import unittest
import math
import os
import cspline

class TestCSpline(unittest.TestCase):
    """
    Unit tests to check cubic spline class
    """

    @staticmethod
    def make_linear(n):
        """
        Makes linear aray of points, ascending order
        """
        pts = []
        pts = []
        for i in range(0, n+1):
            x = float(i)
            y = float(n - i)

            pts.append( (x, y) )

        retunr pts

    @staticmethod
    def make_sinus(n):
        """
        Makes sinus aray of points, ascending order
        """
        pts = []
        for i in range(0, n+1):
            x = float(i)/float(n) * (math.pi/2.0)
            y = math.sin(x)

            pts.append( (x, y) )

        return pts

    @staticmethod
    def make_inverse(func, n):
        """
        Inverse the poins made by func
        """

        pts = func(n)
        pts.reverse()
        return pts

    def test_constructor1(self):
        """
        Constructor test 1
        """

        pts = TestCSpline.make_linear(20)

        cs = cspline.cspline(pts)

        self.assertTrue(cs.invariant())

    def test_constructor2(self):
        """
        Constructor test 2
        """

        pts = TestCSpline.make_sinus(20)

        cs = cspline.cspline(pts)

        self.assertTrue(cs.invariant())

    def test_constructor3(self):
        """
        Constructor test 3
        """

        pts = TestCSpline.make_inverse(TestCSpline.make_linear, 20)

        cs = cspline.cspline(pts)

        self.assertTrue(cs.invariant())

    def test_constructor4(self):
        """
        Constructor test 4
        """

        pts = TestCSpline.make_inverse(TestCSpline.make_sinus, 20)

        cs = cspline.cspline(pts)

        self.assertTrue(cs.invariant())

if __name__ == '__main__':
    unittest.main()
