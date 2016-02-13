# -*- coding: utf-8 -*-

import unittest

from XcIO import Read3ddose

class Test_Read3ddose(unittest.TestCase):

    def test_Read3ddose_calledWithInvalidFileName_shouldRaiseException(self):
        """
        """
        with self.assertRaises(IOError) as context:
            Read3ddose.Read3ddose("D:\Python_tests\pathtounknownfile.3ddose")
        self.assertTrue('Invalid file name' in context.exception)

    def test_Read3ddose_calledWithValidFileNameButWrongStructure_shouldFail(self):
        """
        """
        with self.assertRaises(ValueError) as context:
            Read3ddose.Read3ddose("D:\Python_tests\README.txt")
        self.assertTrue('Invalid file format' in context.exception)

if __name__ == '__main__':
    unittest.main()
