# -*- coding: utf-8 -*-
"""
Created on Tue May 26 15:32:55 2015 by Florin.Neacsu

Copyright Xcision LLC.
"""

import unittest
from XcIO import ReadOCPparam




class Test_ReadICPparam(unittest.TestCase):
    
    def test_ReadICPparam_invalidFileName_shouldRaiseException(self):
        with self.assertRaises(IOError) as context:
            ReadOCPparam.ReadOCPparam("D:\Python_tests\pathtounknownfile.3ddose")
        self.assertTrue('Invalid file name' in context.exception)
    
#    def test_ReadICPparam_fileContainsInvalidParameters_shouldRaiseException(self):
#        with self.assertRaises(ValueError) as context:
#            ReadICPparam.ReadICPparam("D:\Python_tests\R8O2IM01_fake.icpparam")
#        self.assertTrue('Invalid file format' in context.exception)

if __name__ == '__main__':
    unittest.main()