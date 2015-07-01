# -*- coding: utf-8 -*-

import unittest
import phandim

class TestPhanDim(unittest.TestCase):
    """
    Unit tests to check phantom dimensions
    """
    
    def test_constructor1(self):
        bx = [1,2,3,4,5]
        by = [3,2,5,1,6]
        bz = [8,5,23,9,4,3]
        
        pd = phandim.phandim(bx, by, bz)
        
        self.assertTrue(phandim.phandim.check_sorted(pd.bx()))
        self.assertTrue(phandim.phandim.check_sorted(pd.by()))
        self.assertTrue(phandim.phandim.check_sorted(pd.bz()))        

    def test_constructor2(self):
        bx = None
        by = [3,2,5,1,2]
        bz = [8,5,23,8,4,3]
        
        with self.assertRaises(RuntimeError):
            phandim.phandim(bx, by, bz)
            
    def test_constructor3(self):
        bx = [3,2,5,1,2]
        by = None
        bz = [8,5,23,8,4,3]
        
        with self.assertRaises(RuntimeError):
            phandim.phandim(bx, by, bz)

    def test_constructor4(self):
        bx = [3,2,5,1,2]
        by = [8,5,23,8,4,3]
        bz = None
        
        with self.assertRaises(RuntimeError):
            phandim.phandim(bx, by, bz)

    def test_access1(self):
        bx = [3,2,5,1,2]
        by = [8,5,23,8,4,3]
        bz = [8,5,23,9,4,3,90]
        
        pd = phandim.phandim(bx, by, bz)
        
        self.assertTrue( pd.nx() == len(bx)-1 )
        self.assertTrue( pd.ny() == len(by)-1 )
        self.assertTrue( pd.nz() == len(bz)-1 )
        

if __name__ == '__main__':
    unittest.main()
    
