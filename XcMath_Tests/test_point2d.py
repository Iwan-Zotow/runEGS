# -*- coding: utf-8 -*-

import unittest
import numpy as np

import point2d

class TestPoint2D(unittest.TestCase):
    """
    Unit tests to check point2d
    """
    
    def test_constructor1(self):
        """
        constructor test 1
        """        

        pt = point2d.point2d()
        
        self.assertTrue(pt.x() == np.float32(0.0))
        self.assertTrue(pt.y() == np.float32(0.0))

    def test_constructor2(self):
        """
        constructor test 2
        """        

        pt = point2d.point2d(2.1, 7.3)
        
        self.assertTrue(pt.x() == np.float32(2.1))
        self.assertTrue(pt.y() == np.float32(7.3))

if __name__ == '__main__':
    unittest.main()
