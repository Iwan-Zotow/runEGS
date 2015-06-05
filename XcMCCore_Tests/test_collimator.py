# -*- coding: utf-8 -*-

import unittest
import collimator

class TestCollimator(unittest.TestCase):
    """
    Unit tests to check collimator
    """
    
    def test_constructor1(self):
        """
        Constructor test 1
        """
        cc = collimator.collimator(25)
        
        self.assertTrue(cc.size() == 25)

    def test_constructor2(self):
        """
        Constructor test 2
        """
        cc = collimator.collimator(15)
        
        self.assertTrue(cc.size() == 15)
        
    def test_constructor3(self):
        """
        Constructor test 3
        """
        cc = collimator.collimator(0)
        
        self.assertTrue(cc.size() == 0)

    def test_constructor4(self):
        """
        Constructor test 4
        """
        with self.assertRaises(ValueError):
            cc = collimator.collimator(-1)
            
    def test_lt(self):
        """
        Test less than ordering
        """
        cc25 = collimator.collimator(25)
        cc15 = collimator.collimator(15)
        
        self.assertTrue(cc15 < cc25)
        self.assertFalse(cc25 < cc15)

    def test_gt(self):
        """
        Test less than ordering
        """
        cc25 = collimator.collimator(25)
        cc15 = collimator.collimator(15)
        
        self.assertTrue(cc25 > cc15)
        self.assertFalse(cc15 > cc25)

    def test_eq(self):
        """
        Test equivalence
        """
        cc25  = collimator.collimator(25)
        cc15  = collimator.collimator(15)
        ccc25 = collimator.collimator(25)
        
        self.assertTrue(cc25 == ccc25)
        self.assertFalse(cc25 == cc15)

    def test_ne(self):
        """
        Test non-equivalence
        """
        cc25  = collimator.collimator(25)
        ccc25 = collimator.collimator(25)
        cc15  = collimator.collimator(15)
        
        self.assertTrue(cc25 != cc15)
        self.assertFalse(cc25 != ccc25)

    def test_str(self):
        """
        Test string conversion
        """
        cc = collimator.collimator(25)
        ss = str(cc)
        
        self.assertTrue(ss == "C25")

if __name__ == '__main__':
    unittest.main()
