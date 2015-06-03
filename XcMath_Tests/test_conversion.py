# -*- coding: utf-8 -*-

import numpy as np
import unittest
import conversion

class TestConversion(unittest.TestCase):
    """
    Unit tests to check conversion
    """
    
    def test_cm2mm(self):
        """
        test passable cm2mm conversion
        """
        v = 2.0
        r = conversion.cm2mm(v)
        self.assertTrue(r == v*10.0)
        
    def test_cm2mmA(self):
        """
        test not-passable cm2mm conversion
        """
        v = np.NaN
        with self.assertRaises(ValueError):
            conversion.cm2mm(v)
        
    def test_mm2cm(self):
        """
        test passable mm2cm conversion
        """
        v = 2.0
        r = conversion.mm2cm(v)
        self.assertTrue(r == v*0.1)

    def test_mm2cmA(self):
        """
        test not-passable mm2cm conversion
        """
        v = np.NaN
        with self.assertRaises(ValueError):
            conversion.mm2cm(v)

if __name__ == '__main__':
    unittest.main()
