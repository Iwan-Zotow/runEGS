# -*- coding: utf-8 -*-

import unittest
from XcIO import ReadICPparam


"""
I don't like that I am going to a file on hdd
-> I should probably create a temp file
with the appropriate 'wrong' param
use it for the test, the delete it

Too slow (hdd write/read) for a unit test?

  Florin
"""

class Test_ReadICPparam(unittest.TestCase):
    
    def test_ReadICPparam_invalidFileName_shouldRaiseException(self):
        with self.assertRaises(IOError) as context:
            ReadICPparam.ReadICPparam("D:\Python_tests\pathtounknownfile.3ddose")
        self.assertTrue('Invalid file name' in context.exception)
    
    def test_ReadICPparam_fileContainsInvalidParameters_shouldRaiseException(self):
        with self.assertRaises(ValueError) as context:
            ReadICPparam.ReadICPparam("D:\Python_tests\R8O2IM01_fake.icpparam")
        self.assertTrue('Invalid file format' in context.exception)

if __name__ == '__main__':
    unittest.main()
        
