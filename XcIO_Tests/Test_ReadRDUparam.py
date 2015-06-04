# -*- coding: utf-8 -*-
"""
Created on Mon Jun 01 11:40:08 2015 by Florin.Neacsu

Copyright Xcision LLC.
"""

import unittest
from XcIO import ReadRDUparam

class Test_ReadRDUparam(unittest.TestCase):
    
    def test_ReadRDUparam_invalidFileName_shouldRaiseException(self):
        with self.assertRaises(IOError) as context:
            ReadRDUparam.ReadRDUparam("D:\Python_tests\pathtounknownfile.3ddose")
        self.assertTrue('Invalid file name' in context.exception)
    
    def test_ReadRDUparam_fileContainsInvalidParameters_shouldRaiseException(self):
        with self.assertRaises(IndexError) as context:
            ReadRDUparam.ReadRDUparam("D:\Python_tests\R8_fake.rduparam")
        self.assertTrue('Invalid file format' in context.exception)

if __name__ == '__main__':
    unittest.main()