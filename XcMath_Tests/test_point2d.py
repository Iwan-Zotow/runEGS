# -*- coding: utf-8 -*-

import unittest
import point2d

class TestPoint2D(unittest.TestCase):
    """
    Unit tests to check point2d
    """
    
    def test_constructor(self):
        """
        constructor test
        """        

        pt = point2d.point2d()
        
        self.assertTrue(pt.x() == 0.0)
        self.assertTrue(pt.y() == 0.0)

if __name__ == '__main__':
    unittest.main()
