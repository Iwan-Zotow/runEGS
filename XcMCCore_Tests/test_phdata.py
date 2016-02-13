# -*- coding: utf-8 -*-

import unittest

from XcMCCore import phandim
from XcMCCore import phdata

class TestPhantom(unittest.TestCase):
    """
    Unit tests to check phantom dimensions
    """

    def test_constructor1(self):
        bx = [1,2,3,4,5]
        by = [3,2,5,1,6]
        bz = [8,5,23,9,4,3]

        ph = phdata.phdata(bx, by, bz)

        self.assertTrue(phandim.phandim.check_sorted(ph.bx()))
        self.assertTrue(phandim.phandim.check_sorted(ph.by()))
        self.assertTrue(phandim.phandim.check_sorted(ph.bz()))

    def test_constructor2(self):
        bx = None
        by = [3,2,5,1,2]
        bz = [8,5,23,8,4,3]

        with self.assertRaises(RuntimeError):
            phdata.phdata(bx, by, bz)

    def test_constructor3(self):
        bx = [3,2,5,1,2]
        by = None
        bz = [8,5,23,8,4,3]

        with self.assertRaises(RuntimeError):
            phdata.phdata(bx, by, bz)

    def test_constructor5(self):
        bx = [3,2,5,1,2]
        by = [8,5,23,8,4,3]
        bz = None

        with self.assertRaises(RuntimeError):
            phdata.phdata(bx, by, bz)

    def test_access1(self):
        bx = [3,2,5,1,2]
        by = [8,5,23,8,4,3]
        bz = [8,5,23,9,4,3,90]

        ph = phdata.phdata(bx, by, bz)

        self.assertTrue( ph.nx() == len(bx)-1 )
        self.assertTrue( ph.ny() == len(by)-1 )
        self.assertTrue( ph.nz() == len(bz)-1 )


if __name__ == '__main__':
    unittest.main()

