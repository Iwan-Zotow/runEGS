# -*- coding: utf-8 -*-

import math
import cspline

import logging

from XcMCCore.cup import cup
from XcMath import utils

class spline_cup(cup):
    """
    Class to provide specialized cup,
    where model is made from spline approximation between
    base points

    Contains curves for both inner cup and outer cup
    """

    def __init__(self, fname, zshift):
        """
        Init spline cup from the file

        Parameters
        ----------

        fname: string
            base points file name
        """

        super(spline_cup, self).__init__(fname, zshift)

        logging.info("spline_cad::__init__ started")
        logging.debug(str(fname))
        logging.debug(str(zshift))

        self._cspline = None

        self._grad = None

        self._zmin = None

        self.init_from_file()

        # done wih computing, now logging
        logging.info("spline_cad::__init__ constructed")
        logging.debug(str(self._zmax))
        logging.debug(str(self._grad))

    def init_from_file(self):
        """
        Read cup spline base points data from text file
        """

        lines = None
        with open(self._fname) as f:
            lines = f.readlines()

        if lines == None:
            self._cspline = None
            return

        pts = []
        for line in lines:
            s  = line.split()
            x = float(s[0])
            d = float(s[1])
            pts.append((x, d))

        self._cspline = cspline.cspline(pts)

        if not self.invariant():
            raise RuntimeError("cup_cad::__init__", "bad invariant")

        # min and max value where we could
        # compute
        self._zmin = 0.0
        self._zmax = self._cspline.xmax() + self._zshift

        # compute gradient and slope
        za = self._cspline.xmin()
        zb = za + 0.5
        va = self._cspline.calculate(za)
        vb = self._cspline.calculate(zb)

        self._grad = (vb - va) / (zb - za)


    def invariant(self):
        """
        Checks if data are consistent

        Parameters
        ----------

        self: spline_cup
            this
        returns: boolean
            True if ok, False otherwise
        """

        if (not self._cspline.invariant()):
            return False

        if self._zmin < 0.0:
            return False

        return True


    def cspline(self):
        return self._cspline

    def curve(self, z):
        """
        For given Z, return positive Y on the inner cup curve

        Parameters
        ----------

        self: inner_cup
            this

        z: double
            position along the cup axis

        returns: double
            cup radius at given Z
        """

        if z < 0.0:
            return -2.0

        if z > self._zmax:
            return -1.0

        if z == self._zmax:
            return 0.0

        if z < self._zmin: # linear interpolation
            return self._b + self._k * (z - self._zmin)

        # in the spline region
        return self._cspline.calculate(z)


    def classify(self, r, z):
        """
        Classification of the point relative to the cup

        -1 - outside
         0 - in the cup
        +1 - inside

        Parameters
        ----------

        r: double
            radial coordinate

        z: double
            vertical coordinate, going down from top to the tip of the cup

        returns: int
            classification
        """

        # using symmetry to set radial coordinate
        r = math.fabs(r)

        Rin = self.curve(z)
        if Rin == -2.0:
            return cup.OUTSIDE
        if Rin == 0.0:
            return cup.INTHECUP
        if r <= Rin:
            return cup.INSIDE

        return cup.OUTSIDE

if __name__ == "__main__":

    cup = spline_cup("C:/Users/kriol/Documents/Python/runEGS/cup_geometry/R8O2IM01_KddCurveA _Spline.txt")

    for k in range(0, 1000):
        z = 1.0 * float(k)
        r = cup.get_outer_curve(z)
        if r < 0.0:
            break

        print("   {0}   {1}".format(z, r))
