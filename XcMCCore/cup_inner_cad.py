# -*- coding: utf-8 -*-

import math
import logging

import numpy as np

from XcMCCore.cup import cup

from XcMath       import utils
from XcMath       import point2d
from XcIO         import ReadICPparam
from XcIO         import disc_2d
from XcMath       import linint

class cup_inner_cad(cup):
    """
    Class to provide specialized cup,
    where model is made from CAD curves and lines

    Contains curves for both inner inner cup and inner outer cup
    """

    def __init__(self, fname, zshift = 0.0, use_cup = cup.USE_OUTER):
        """
        Inner ICPPARAM cup data constructor

        Parameters
        ----------

        fname: string
            ICPPARAM file name

        zshift: float
            inner cup Z shift, mm
        """

        super(cup_inner_cad, self).__init__(fname, zshift)

        logging.info("cup_inner_cad::__init__ started")
        logging.debug(str(fname))
        logging.debug(str(zshift))
        logging.debug(str(use_cup))

        self._use_cup = use_cup

        self._RU = None
        self._OC = None
        self._ICType = None
        self._ICSize = None
        self._ZOffset  = None
        self._ICOrigin = None
        self._ICWallEncodingType       = None
        self._ICInsideWallDescription  = None
        self._ICOutsideWallDescription = None

        self._xiw  = None
        self._yiw  = None
        self._xciw = None
        self._yciw = None
        self._xxiw = None
        self._yyiw = None

        self._xow  = None
        self._yow  = None
        self._xcow = None
        self._ycow = None
        self._xxow = None
        self._yyow = None

        self._linint_iw = None
        self._linint_ow = None

        self.init_from_file()

        pts = [point2d.point2d(np.float32(x), np.float32(y)) for x, y in zip(self._xxiw,  self._yyiw)]

        self._linint_iw = linint.linint(point2d.point2d.remove_dupes(pts, np.float32(0.00001)))

        pts = [point2d.point2d(np.float32(x), np.float32(y)) for x, y in zip(self._xxow,  self._yyow)]

        self._linint_ow = linint.linint(point2d.point2d.remove_dupes(pts, np.float32(0.00001)))

        self._zmax = self._linint_ow.zmax() + self._zshift

        if not self.invariant():
            raise RuntimeError("cup_inner_cad::__init__", "bad invariant")

        # done wih computing, now logging
        logging.info("cup_inner_cad::__init__ constructed")

    def init_from_file(self):
        """
        Read cup data from CAD file
        """

        logging.info("cup_inner_cad::init_from_file enter")

        data = None
        with open(self._fname) as f:
            try:
                RU, OC, ICType, ICSize, ZOffset, ICOrigin, ICWallEncodingType, ICInsideWallDescription, ICOutsideWallDescription = ReadICPparam.ReadICPparam(self._fname)
            except Exception as e:
                e.args += ('cup_inner_cad::Bad read of inner cup',)
                raise

        self._RU = RU
        self._OC = OC
        self._ICType   = ICType
        self._ICSize   = ICSize
        self._ZOffset  = ZOffset
        self._ICOrigin = ICOrigin
        self._ICWallEncodingType       = ICWallEncodingType
        self._ICInsideWallDescription  = ICInsideWallDescription
        self._ICOutsideWallDescription = ICOutsideWallDescription

        # those arrays are NumPy arrays
        self._xiw, self._yiw, self._xciw, self._yciw = disc_2d.disc_2d(self._ICInsideWallDescription, 0.5)
        self._xow, self._yow, self._xcow, self._ycow = disc_2d.disc_2d(self._ICOutsideWallDescription, 0.5)

        # ? all data we have is of type 1
        # ? no chenches to outer wall
        #if self._ICWallEncodingType == 2:
        #    self._xow = self.xow - self._ICOrigin[0]
        #    self._yow = self.yow - self._ICOrigin[1]
        #    self._xcow = self.xcow - self._ICOrigin[0]
        #    self._ycow = self.ycow - self._ICOrigin[1]

        self.convert_to_ICP()

        logging.info("cup_inner_cad::init_from_file done")

    def convert_to_ICP(self):
        """
        Take digitized curves and convert then to .ICP format
        """

        yo = self._yiw[0]

        self._xxiw = -(self._yiw - yo) - self._ZOffset
        self._yyiw = self._xiw[:]

        self._xxow = -(self._yow - yo) - self._ZOffset
        self._yyow = self._xow[:]

    def invariant(self):
        """
        Checks validity of the input

        Parameters
        ----------

            returns: boolean
                True if ok, False otherwise
        """

        logging.info("cup_inner_cad::invariant")

        # at the end, only linear interpolator matters
        if not self._linint_iw.invariant():
            return False
        if not self._linint_ow.invariant():
            return False

        if self._use_cup != cup.USE_INNER and self._use_cup != cup.USE_OUTER:
            return False

        return True

    def linint_ow(self):
        """
        Outer wall interpolator
        """
        return self._linint_ow

    def linint_iw(self):
        """
        Inner wall interpolator
        """
        return self._linint_iw

    def inner_curve(self, z):
        """
        For given Z, return positive R on the external cup curve

        Parameters
        ----------

        z: float
            position along the axis

        returns: float
            Radial position, negative value if outside the cup`
        """
        logging.debug(str(z))

        if z > self._zmax:
            return 0.0

        return self._linint_iw.extrapolate(z - self._zshift)

    def outer_curve(self, z):
        """
        For given Z, return positive R on the external cup curve

        Parameters
        ----------

        z: float
            position along the axis

        returns: float
            Radial position, negative value if outside the cup`
        """
        logging.debug(str(z))

        if z > self._zmax:
            return 0.0

        return self._linint_ow.extrapolate(z - self._zshift)

    def curve(self, z):
        """
        For given Z, return positive R on the external cup curve

        Parameters
        ----------

        z: float
            position along the axis

        returns: float
            Radial position, negative value if outside the cup`
        """

        if self._use_cup == cup.USE_INNER:
            return self.inner_curve(z)

        return self.outer_curve(z)

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

    cup = cup_inner_cad("C:/Users/kriol/Documents/Python/runEGS/CADCups/InnerCups/In/R8O3IL08.icpparam")

    print(cup._RU)
    print(cup._OC)
    print(cup._ICType)
    print(cup._ICSize)
    print(cup._ZOffset)
    print(cup._ICOrigin)
    print(cup._ICWallEncodingType)
    print(cup._ICInsideWallDescription)
    print(cup._ICOutsideWallDescription)

    for x, y in map(lambda x, y: (x,y), cup._xxiw, cup._yyiw):
        print(x, y)
    print("========================")
    for x, y in map(lambda x, y: (x,y), cup._xxow, cup._yyow):
        print(x, y)
