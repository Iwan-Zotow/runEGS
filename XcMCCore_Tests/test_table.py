# -*- coding: utf-8 -*-

import unittest
import table

class TestTable(unittest.TestCase):
    """
    Unit tests to test table
    """

    def test_constructor1(self):
        """
        Constructor test 1
        """
        tbl = table.table("/home/kriol/Documents/EGS/runEGS/cup_geometry/Table.json")

        # print(tbl)

        self.assertTrue(tbl.invariant())

    def test_outside1(self):
        """
        Test point outside
        """
        tbl = table.table("/home/kriol/Documents/EGS/runEGS/cup_geometry/Table.json")

        self.assertFalse(tbl.is_inside(10000.0, 0.0))

    def test_outside2(self):
        """
        Test point outside
        """
        tbl = table.table("/home/kriol/Documents/EGS/runEGS/cup_geometry/Table.json")

        self.assertFalse(tbl.is_inside(120.0, -10.0))

    def test_outside3(self):
        """
        Test point outside
        """
        tbl = table.table("/home/kriol/Documents/EGS/runEGS/cup_geometry/Table.json")

        self.assertFalse(tbl.is_inside(120.0, 999.0))

    def test_indise1(self):
        """
        Test point outside
        """
        tbl = table.table("/home/kriol/Documents/EGS/runEGS/cup_geometry/Table.json")

        self.assertTrue(tbl.is_inside(110.0, 20.0))

if __name__ == '__main__':
    unittest.main()
