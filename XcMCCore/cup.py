# -*- coding: utf-8 -*-

class cup(object):
    """
    This class is the base class for the cup.
    Contains
    """

    OUTSIDE  = -1
    INTHECUP =  0
    INSIDE   = +1

    def __init__(self, fname, zshift = 0.0):
        """
        Constructor
        """
        self._zmax   = None
        self._zshift = zshift

        self._fname = fname

    def zmax(self):
        return self._zmax

    def zshift(self):
        return self._zshift

    def zshift(self):
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
        raise NotImplementedError("cup.classify: method not implemented")

    def init_from_file(self):
        """
        Read cup data from JSON file

        Parameters
        ----------

            self: inner_cup
                this
        """
        raise NotImplementedError("cup.init_from_file: method not implemented")

    def curve(self, z):
        """
        For given Z, return positive R on the outer cup curve

        Parameters
        ----------

            z: double
                position along the axis

            returns: double
                Radial position, negative i`
        """
        raise NotImplementedError("cup.curve: method not implemented")
