# -*- coding: utf-8 -*-

import os
import logging

import numpy as np
from XcMath import point2d as pt

class curve(object):
    """
    Load and check cup curve
    """

    def __init__(self, fname):
        """
        Constructor. Build curve from file data

        Parameters
        ----------

        fname: string
            filename to load data from
        """

        logging.info("Start curve construction")
        logging.debug(fname)

        self._curve = None

        if fname == None:
            raise ValueError("curve", "Null file name")

        if not os.path.isfile(fname):
            raise ValueError("curve", "No such file")

        lines = []
        with open(fname, "rt") as f:
            lines = f.readlines()

        if len(lines) == 0:
            raise RuntimeError("curve", "No lines were read from file")

        if len(lines) == 1:
            raise RuntimeError("curve", "Cup file contains single line")

        self._curve = []
        for line in lines:
            split = line.split(" ")
            split = [x for x in split if x] # remove empty lines
            zr = pt.point2d(np.float32(split[0]), np.float32(split[1]))
            self._curve.append( zr )

        # last point from some fixup in make_cup
        ptl  = self._curve[-1]
        ptll = self._curve[-2]

        zr = pt.point2d(2.0*ptl.x() - ptll.x(), 2.0*ptl.y() - ptll.y())
        self._curve.append( zr )

        if not self.invariant():
            raise RuntimeError("cup_curve", "Data not consistent")

        logging.info("Done curve construction")
        logging.debug(str(self))

    def __getitem__(self, i):
        """
        Returns point at given index

        Parameters
        ----------

        i: integer
            index to get point from

        returns: point2d
            point at index at the curve
        """
        logging.debug("curve.__getitem__({0})".format(i))
        return self._curve[i]

    def invariant(self):
        """
        Check if data is consistent

        returns: boolean
            true if ok, false otherwise
        """
        for d in self._curve:
            p = d
            if np.isnan( p.x() ):
                return False
            if np.isnan( p.y() ):
                return False
            if p.y() < 0.0: # second coordinate is radius, cannot be negative
                return False

        return True

    def curve(self):
        """
        Returns curve

        returns: array of points
            array of cup points
        """
        return self._curve

    def __len__(self):
        """
        Returns curve length

        returns: integer
            curve length
        """
        return len(self._curve)

    def __str__(self):
        """
        """
        s = ""
        for p in self._curve:
            s += str(p) + "\n"
        return s

