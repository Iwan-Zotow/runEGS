# -*- coding: utf-8 -*-

import math
import cspline

class spline_cup(object):
    """
    This class is used to model cup with few points describing
    """

    def __init__(self, fname):
        """
        Init spline cup from the file

        Parameters
        ----------

        fname: string
            base points file name
        """

        self._fname = fname

        self._cspline = None

        # maximum Z value
        self._zmax = None

        self._zmin = None

        self._k = None
        self._b = None

        self.init_from_file()

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

    def init_from_file(self):
        """
        Read cup data from text file

        Parameters
        ----------

        self: inner_cup
            this
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

        # min and max value where we could
        # compute
        self._zmax = self._cspline.xmax()
        self._zmin = self._cspline.xmin()

        # compute gradient and slope
        self._k = (self._cspline.calculate(self._zmin + 0.5) - self._cspline.calculate(self._zmin)) / 0.5
        self._b = self._cspline.calculate(self._zmin)

        if not self.invariant():
            raise Exception("Data ARE INCONSISTENT")

    def cspline(self):
        return self._cspline

    def zmax(self):
        return self._zmax

    def get_outer_curve(self, z):
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

        Rin = self.get_outer_curve(z)
        if Rin == -2.0:
            return -1
        if Rin == 0.0:
            return 0
        if r <= Rin:
            return +1

        return -1

if __name__ == "__main__":

    cup = spline_cup("C:/Users/kriol/Documents/Python/runEGS/cup_geometry/R8O2IM01_KddCurveA _Spline.txt")

    for k in range(0, 1000):
        z = 1.0 * float(k)
        r = cup.get_outer_curve(z)
        if r < 0.0:
            break

        print("   {0}   {1}".format(z, r))
