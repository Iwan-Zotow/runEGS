# -*- coding: utf-8 -*-

import unittest

from XcMath import utils

class TestUtils(unittest.TestCase):
    """
    Unit tests to check utils
    """

    def test_squared(self):
        """
        test passable squaring
        """
        v = 2.0
        r = utils.squared(v)
        self.assertTrue(r == 2.0*2.0)

    def test_cubed(self):
        """
        test passable cubing
        """
        v = 2.0
        r = utils.cubed(v)
        self.assertTrue(r == 2.0*2.0*2.0)

if __name__ == '__main__':
    unittest.main()
