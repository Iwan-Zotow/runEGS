# -*- coding: utf-8 -*-

import logging

class cup(object):
    """
    This class is the base class for the cup.
    Contains base methods tobe reimplemented in the child classes
    """

    OUTSIDE  = -1
    INTHECUP =  0
    INSIDE   = +1

    def __init__(self, fname, zshift = 0.0):
        """
        Construct the cup with init name and zshift

        Parameters
        ----------

        fname: string
            init file name

        zshift: double
            inner cup Z shift, mm
        """

        self._zmax   = None
        self._zshift = zshift

        self._fname = fname

        logging.info("cup::__init__")
        logging.debug(str(fname))
        logging.debug(str(zshift))

    def init_from_file(self):
        """
        Read cup data from init file
        """
        raise NotImplementedError("cup::init_from_file: method not implemented")

    def invariant(self):
        """
        Checks validity of the input

        Parameters
        ----------

            returns: boolean
                True if ok, False otherwise
        """
        raise NotImplementedError("cup::invariant: method not implemented")

    def zmax(self):
        """
        Returns Z max
        """
        return self._zmax

    def zshift(self):
        """
        Returns Z shift
        """
        return self._zshift

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
        raise NotImplementedError("cup::classify: method not implemented")


    def curve(self, z):
        """
        For given Z, return positive R on the external cup curve

        Parameters
        ----------

            z: double
                position along the axis

            returns: double
                Radial position, negative value if outside the cup`
        """
        raise NotImplementedError("cup::curve: method not implemented")
