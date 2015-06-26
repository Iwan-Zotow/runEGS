# -*- coding: utf-8 -*-

import math
import unittest
import voxarea

class TestVoxarea(unittest.TestCase):
    """
    Unit tests to check voxel area
    """        
    
    def test_circ_segment_area1(self):
        """
        test circ_segment_area 1
        check if at zero height we have half of a circle area
        """
        
        R = 7.0
        h = 0.0
        
        self.assertTrue(voxarea.circ_segment_area(R, h) == 0.25*math.pi*R*R)
        
    def test_circ_segment_area2(self):
        """
        test circ_segment_area 2
        check if at full height we have zero area
        """
        
        R = 7.0
        h = R
        
        self.assertTrue(voxarea.circ_segment_area(R, h) == 0.0)

    def test_circ_segment_area3(self):
        """
        test circ_segment_area 3
        negative radius cause exception
        """
        
        R = -7.0
        h = 2.0
        
        with self.assertRaises(ValueError):
            v = voxarea.circ_segment_area(R, h)
        
    def test_circ_segment_area4(self):
        """
        test circ_segment_area 4
        negative height cause exception
        """
        
        R = 2.0
        h = -1.0
        
        with self.assertRaises(ValueError):
            v = voxarea.circ_segment_area(R, h)
            
    def test_rotate_voxel0(self):
        """
        check voxel rotation 0
        Quarter #0
        """
        
        (xmin, ymin, xmax, ymax) =(0.5, 0.9, 12., 17.)
        
        (xxmin, yymin, xxmax, yymax) = voxarea.rotate_voxel(xmin, ymin, xmax, ymax)
        
        self.assertTrue(xmin == xxmin and ymin == yymin and xmax == xxmax and ymax == yymax)
            
    def test_rotate_voxel1(self):
        """
        check voxel rotation 1
        Quarter #1
        """
        
        xmin, ymin, xmax, ymax = (-9.5, 2.9, -7., 6.0)        
        
        (xxmin, yymin) = voxarea.rotate( xmin, ymin, voxarea.mtxQ1)
        (xxmax, yymax) = voxarea.rotate( xmax, ymax, voxarea.mtxQ1)
        xxxmin = min(xxmin, xxmax)
        xxxmax = max(xxmin, xxmax)
        yyymin = min(yymin, yymax)
        yyymax = max(yymin, yymax)
        
        (xmin, ymin, xmax, ymax) = voxarea.rotate_voxel(xmin, ymin, xmax, ymax)

        self.assertTrue(xmin == xxxmin and ymin == yyymin and xmax == xxxmax and ymax == yyymax)

    def test_rotate_voxel2(self):
        """
        check voxel rotation 2
        Quarter #2
        """
        
        xmin, ymin, xmax, ymax = (-9.5, -6.9, -7., -5.0)
        
        (xxmin, yymin) = voxarea.rotate( xmin, ymin, voxarea.mtxQ2)
        (xxmax, yymax) = voxarea.rotate( xmax, ymax, voxarea.mtxQ2)
        xxxmin = min(xxmin, xxmax)
        xxxmax = max(xxmin, xxmax)
        yyymin = min(yymin, yymax)
        yyymax = max(yymin, yymax)
        
        (xmin, ymin, xmax, ymax) = voxarea.rotate_voxel(xmin, ymin, xmax, ymax)

        self.assertTrue(xmin == xxxmin and ymin == yyymin and xmax == xxxmax and ymax == yyymax)

    def test_rotate_voxel3(self):
        """
        check voxel rotation 3
        Quarter #3
        """
        
        xmin, ymin, xmax, ymax = ( 4.5, -6.9, 7., -5.0)
        
        (xxmin, yymin) = voxarea.rotate( xmin, ymin, voxarea.mtxQ3)
        (xxmax, yymax) = voxarea.rotate( xmax, ymax, voxarea.mtxQ3)
        xxxmin = min(xxmin, xxmax)
        xxxmax = max(xxmin, xxmax)
        yyymin = min(yymin, yymax)
        yyymax = max(yymin, yymax)
        
        (xmin, ymin, xmax, ymax) = voxarea.rotate_voxel(xmin, ymin, xmax, ymax)

        self.assertTrue(xmin == xxxmin and ymin == yyymin and xmax == xxxmax and ymax == yyymax)

if __name__ == '__main__':
    unittest.main()
