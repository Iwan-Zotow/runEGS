# -*- coding: utf-8 -*-

import json

class table(object):
    """
    Representation of the table outside the cup
    """

    def __init__(self, fname):
        """
        Initialize the table from JSON file
        """

        self._outer_radius     = -1.0
        self._inner_top_radius = -1.0
        self._inner_bot_radius = -1.0
        self._top_position     = -1.0
        self._bot_position     = -1.0
        self._material         = ""
        self._density          = -1.0

        self._thickness        = -1.0

        otr, itr, ibr, tp, bp, mat, den = table.read_json(fname)

        self._outer_radius     = otr
        self._inner_top_radius = itr
        self._inner_bot_radius = ibr
        self._top_position     = tp
        self._bot_position     = bp
        self._material         = mat
        self._density          = den

        self._thickness        = self._bot_position - self._top_position

        if not self.invariant():
            raise ValueError("Not passed the invariant check" )

    def invariant(self):
        """
        True if ok, False otherwise
        """
        if self._outer_radius <= 0.0:
            return (False, "outer_radius negaitve")
        if self._inner_top_radius <= 0.0:
            return (False, "inner_top_radius negative")
        if self._inner_bot_radius <= 0.0:
            return (False, "inner_bot_radius negative")
        if self._top_position <= 0.0:
            return (False, "top_position negative")
        if self._bot_position <= 0.0:
            return (False, "bot_position negative")
        if self._material == "":
            return (False, "material undefined")
        if self._density <= 0.0:
            return (False, "density negative")
        if self._inner_bot_radius > self._inner_top_radius:
            return (False, "bottom radius larger than top radius")

        if self._thickness <= 0.0:
            return (False, "thickness negative")

        return True

    @staticmethod
    def read_json(fname):
        """
        read and parse JSON
        """

        rc = None

        with open(fname, "r") as f:
            data = json.load(f)

            otr = data["outer_radius"]
            itr = data["inner_top_radius"]
            ibr = data["inner_bot_radius"]
            tp  = data["top_position"]
            bp  = data["bot_position"]
            mat = data["material"]
            den = data["density"]

            rc = (otr, itr, ibr, tp, bp, mat, den)

        return rc

    def density(self):
        return self._density

    def density(self):
        return self._density

    def is_inside(self, r, z):
        """
        Classification routine
        Returns True if point is inside, False otherwise
        """

        if z < self._top_position:
            return False

        if z > self._bot_position:
            return False

        if r > self._outer_radius:
            return False

        if r < self._inner_bot_radius: # smallest of the inner radii
            return False

        # build intermediate inner radius
        p = (z - self._top_position) / self._thickness
        q = 1.0 - p
        assert(p >= 0.0 and p <= 1.0)

        ir = p * self._bot_position + q * self._top_position

        if r < ir:
            return False

        return True

    def __str__(self):
        """
        Return string representation
        """
        return str(self._outer_radius) + " " + \
               str(self._inner_top_radius) + " " + \
               str(self._inner_bot_radius) + " " + \
               str(self._top_position) + " " + \
               str(self._bot_position) + " " + \
               str(self._material) + " " + \
               str(self._density) + " " + \
               str(self._thickness)

    def __repr__(self):
        """
        Return internal representation
        """
        return self.__str__()
