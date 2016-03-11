# -*- coding: utf-8 -*-

import logging

from XcMCCore.cup import cup

from XcMath import utils
from XcMath import curve
from XcMath import linint

class cup_linint(cup):
    """
    Class to provide specialized cup,
    where model is made from linear interpolation
    between set of points

    Contains curves for the outer cup only
    """

    def __init__(self, fname, zshift = 0.0):
        """
        Constructor for linear interpolation cup

        Parameters
        ----------

        fname: string
            file name to read points

        zshift: float
            inner cup Z shift, mm
        """

        super(cup_linint, self).__init__(fname, zshift)

        logging.info("cup_linint::__init__ started")
        logging.debug(str(fname))
        logging.debug(str(zshift))

        self._linint = None

        self.init_from_file()

        self._zmax = self._linint.zmax() + self._zshift

    def init_from_file(self):
        """
        Read cup data from text file
        """

        logging.info("cup_linint::init_from_file")
        logging.debug(str(self._fname))

        cc  = curve.curve( self._fname )
        if cc == None:
            raise RuntimeError("cup_linint::init_from_file", "No curve was constructed")

        self._linint = linint.linint(cc)

    def invariant(self):
        """
        Checks validity of the input

        Parameters
        ----------

            returns: boolean
                True if ok, False otherwise
        """

        logging.info("cup_linint::invariant")

        if not self._linint.invariant():
            return False

        return True

    def linint(self):
        """
        Returns linear interpolator
        """
        return self._linint

    def curve(self, z):
        """
        For given Z, return positive R on the external cup curve

        Parameters
        ----------

        Parameters
        ----------

        z: float
            position along the axis

        returns: float
            Radial position, negative value if outside the cup`
        """
        #logging.info("cup_linint::curve")
        logging.debug(str(z))

        if z > self._zmax:
            return 0.0

        return self._linint.extrapolate(z - self._zshift)

    def classify(self, rr, z):
        """
        Classification of the point relative to the cup

        -1 - outside
         0 - in the cup
        +1 - inside

        Parameters
        ----------

            rr: double
                radial coordinate

            z: double
                vertical coordinate, going down from top to the tip of the cup

            returns: int
                classification
        """

        logging.info("cup_linint::classify")
        logging.debug(str(z))
        logging.debug(str(rr))

        # using symmetry to set radial coordinate
        r = math.fabs(rr)

        Rin = self.inner_curve(z - self._zshift)
        if Rin == -2.0:
            return cup.OUTSIDE
        if Rin == 0.0:
            return cup.INTHECUP
        if r <= Rin:
            return cup.INSIDE

        # could be inside the outer curve
        Rout = self.outer_curve(z)
        if Rout == -2.0:
            return cup.OUTSIDE
        if r <= Rout:
            return cup.INTHECUP

        return cup.OUTSIDE

    def classify(self, rr, z):
        """
        Classification of the point relative to the cup

        -1 - outside
         0 - in the cup
        +1 - inside

        Parameters
        ----------

            rr: double
                radial coordinate

            z: double
                vertical coordinate, going down from top to the tip of the cup

            returns: int
                classification
        """

        logging.info("cup_linint::classify")
        logging.debug(str(z))
        logging.debug(str(rr))

        # using symmetry to set radial coordinate
        r = math.fabs(rr)

        if z > self._zmax:
            return cup.OUTSIDE

        if z < 0.0:
            return cup.OUTSIDE

        R = self.curve(z)

        if R < 0.0:
            return cup.OUTSIDE
        if r <= R:
            return cup.INSIDE

        return cup.OUTSIDE

if __name__ == "__main__":
    import sys

    sys.exit(0)
