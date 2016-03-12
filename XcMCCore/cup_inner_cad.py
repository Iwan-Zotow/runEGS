# -*- coding: utf-8 -*-

import math
import json

import logging

from XcMCCore.cup import cup
from XcMath       import utils
from XcIO         import ReadICPparam

class cup_inner_cad(cup):
    """
    Class to provide specialized cup,
    where model is made from spherical curves and lines

    Contains curves for both inner cup and inner cup
    """

    def __init__(self, fname, zshift = 0.0):
        """
        Curves cup data constructor

        Parameters
        ----------

        fname: string
            JSON file name

        zshift: float
            inner cup Z shift, mm
        """

        super(cup_inner_cad, self).__init__(fname, zshift)

        logging.info("cup_inner_cad::__init__ started")
        logging.debug(str(fname))
        logging.debug(str(zshift))

        self._RU = None
        self._OC = None
        self._ICType = None
        self._ICSize = None
        self._ZOffset  = None
        self._ICOrigin = None
        self._ICWallEncodingType       = None
        self._ICInsideWallDescription  = None
        self._ICOutsideWallDescription = None

        self.init_from_file()
        if not self.invariant():
            raise RuntimeError("cup_inner_cad::__init__", "bad invariant")

        self._zmin = 0.0
        self._zmax = 0.0

        # done wih computing, now logging
        logging.info("cup_inner_cad::__init__ constructed")
        logging.debug(str(self._zmin))
        logging.debug(str(self._zmax))

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
        self._ICType = ICType
        self._ICSize = ICSize
        self._ZOffset = ZOffset
        self._ICOrigin = ICOrigin
        self._ICWallEncodingType       = ICWallEncodingType
        self._ICInsideWallDescription  = ICInsideWallDescription
        self._ICOutsideWallDescription = ICOutsideWallDescription

        logging.info("cup_inner_cad::init_from_file done")

    def invariant(self):
        """
        Checks validity of the input

        Parameters
        ----------

            returns: boolean
                True if ok, False otherwise
        """

        logging.info("cup_inner_cad::invariant")

        return True

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

        logging.info("cup_inner_cad::classify")
        logging.debug(str(z))
        logging.debug(str(rr))

        # using symmetry to set radial coordinate
        r = math.fabs(rr)

        return cup.OUTSIDE

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
        #logging.info("cup_inner_cad::curve")
        logging.debug(str(z))

        if z > self._zmax:
            return 0.0

        if z < self._zmin:
            return 0.0

        return 0.0

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
