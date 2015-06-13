# -*- coding: utf-8 -*-

import unittest
import math
import voxarea

class TestVoxarea(unittest.TestCase):
    """
    Unit tests to check voxel area
    """
    
    def test_circ_segment_area1(self):
        """
        test_circ_segment_area1
        """
        
        R = 7.0
        h = 0.0
        
        self.assertTrue(circ_segment_area(R, h) == 0.25*math.pi*R*R)
        
    def test_circ_segment_area2(self):
        """
        test_circ_segment_area3
        """
        
        R = 7.0
        h = R
        
        self.assertTrue(circ_segment_area(R, h) == 0.0)

    def test_circ_segment_area3(self):
        """
        test_circ_segment_area3
        """
        
        R = -7.0
        h = 2.0
        
        with self.assertRaises(ValueError):
            v = circ_segment_area(R, h)
        
    def test_circ_segment_area4(self):
        """
        test_circ_segment_area4 
        """
        
        R = 2.0
        h = -1.0
        
        with self.assertRaises(ValueError):
            v = circ_segment_area(R, h)
            
if __name__ == '__main__':
    unittest.main()
