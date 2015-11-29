# -*- coding: utf-8 -*-

import math
import json

class inner_cup(object):
    """
    class to describe inner cup
    """

    def __init__(self, fname):
        """
        Inner cup data constructor

        Parameters
        ----------

        fname: string
            JSON file name
        """

        self._fname = fname

        self._cup_series = None
        self._cup_number = -1

        # fixed distance from top, 2.53 mm
        self._H0 = None

        # outer curve
        self._R1 = None
        self._D1 = None
        self._H1 = None

        # inner curve
        self._R2 = None
        self._D2 = None
        self._H2 = None

        self._D5 = None
        self._D6 = None

        # for 0 cups there is another area of transition
        self._D3 = None
        self._H3 = None

        self._D4 = None
        self._H4 = None

        # distance from Dn to the center of the circular part
        self._L1 = None
        self._L2 = None

        # maximum Z value
        self._Z1 = None
        self._Z2 = None

        self.init_from_file()

    @staticmethod
    def get_units_multiplier(data):
        """
        Read units from JSON data

        Parameters
        ----------
            data: dictionary
                JSON cup data

            returns: float
                length multiplier
        """

        u = data.get("units", None)

        if u == "mm":
            return 1.0

        if u == "cm":
            return 10.0

        return -1.0

    def init_from_file(self):
        """
        Read cup data from JSON file

        Parameters
        ----------
        """

        fname = self._fname

        data = None
        with open(fname) as f:
            data = json.load(f)

            # units multiplier
            um = inner_cup.get_units_multiplier(data)

            if um < 0.0:
                raise Exception("No units in the cup JSON")

            self._cup_series = data["cup_series"]
            self._cup_number = data["cup_number"]

            self._H0 = um*data["H0"]

            self._R1 = um*data["R1"]
            self._D1 = um*data["D1"]
            self._H1 = um*data["H1"]

            self._R2 = um*data["R2"]
            self._D2 = um*data["D2"]
            self._H2 = um*data["H2"]

            self._D5 = um*data["D5"]

            try:
                d3 = um*data["D3"]
                d4 = um*data["D4"]
                h3 = um*data["H3"]
                h4 = um*data["H4"]
            except KeyError:
                pass
            else:
                self._D3 = d3
                self._H3 = h3

                self._D4 = d4
                self._H4 = h4

            if not self.invariant():
                raise Exception("Data ARE INCONSISTENT")

            self._L1 = math.sqrt( (self._R1 - 0.5*self._D1)*(self._R1 + 0.5*self._D1) )
            self._L2 = math.sqrt( (self._R2 - 0.5*self._D2)*(self._R2 + 0.5*self._D2) )

            self._Z1 = self._H1 - self._L1 + self._R1
            self._Z2 = self._H2 - self._L2 + self._R2

            # need angle correction?
            self._D6 = self._D5 - 2.0*(self._R1 - self._R2)


    def invariant(self):
        """
        check if data are consistent
        """

        # external radius shall be bigger
        if self._R1 <= self._R2:
            return False

        # cut-off shell be within circle
        if self._D1 > 2.0*self._R1:
            return False

        # cut-off shell be within circle
        if self._D2 > 2.0*self._R2:
            return False

        return True

    def H0(self):
        """
        Return H0
        """
        return self._H0

    def R1(self):
        """
        Return R1
        """
        return self._R1

    def H1(self):
        """
        Return H1
        """
        return self._H1

    def D1(self):
        """
        Return D1
        """
        return self._D1

    def R2(self):
        """
        Return R2
        """
        return self._R2

    def H2(self):
        """
        Return H2
        """
        return self._H2

    def D2(self):
        """
        Return D2
        """
        return self._D2

    def D5(self):
        """
        Return D5
        """
        return self._D5

    def L1(self):
        """
        Return L1
        """
        return self._L1

    def L2(self):
        """
        Return L2
        """
        return self._L2

    def Z1(self):
        """
        Return Z1
        """
        return self._Z1

    def Z2(self):
        """
        Return Z2
        """
        return self._Z2

    def get_inner_curve(self, z):
        """
        For given Z, return positive Y on the inner cup curve

        Parameters
        ----------

            z: double
                position along the axis

            returns: double
                Radial position
        """

        if z < 0.0:
            return -2.0

        if z > self._Z2:
            return -1.0

        if z == self._Z2:
            return 0.0

        if z >= self._H2:
            return math.sqrt( (self._R2 - (z - (self._H2 - self._L2)))*(self._R2 + (z - (self._H2 - self._L2))) )

        k = 0.5* ( self._D2 - self._D6 ) / (self._H2 - self._H0)

        return k * (z - self._H0) + 0.5*self._D6

    def zmin_inner(self):
        """
        Return Z min for inner curve of the cup, mm
        """
        return 0.0

    def zmax_inner(self):
        """
        Return Z max for inner curve of the cup, mm
        """
        return self._Z2

    def zmin_outer(self):
        """
        Return Z min for outer curve of the cup, mm
        """
        return 0.0

    def zmax_outer(self):
        """
        Return Z max for outer curve of the cup, mm
        """
        return self._Z1

    def get_outer_curve(self, z):
        """
        For given Z, return positive Y on the inner cup curve
        """

        if z < 0.0:
            return -2.0

        if z > self._Z1:
            return -1.0

        if z == self._Z1:
            return 0.0

        if z >= self._H1:
            return math.sqrt( (self._R1 - (z - (self._H1 - self._L1)))*(self._R1 + (z - (self._H1 - self._L1))) )

        k = 0.5* ( self._D1 - self._D5 ) / (self._H1 - self._H0)

        return k * (z - self._H0) + 0.5*self._D5

    def classify(self, y, z):
        """
        Y is radial coordinate
        Z is going down from top to the tip of the cup

        classification of the point relative to the cup

        -1 - outside
         0 - in the cup
        +1 - inside
        """

        # using symmetry to set radial coordinate
        r = y
        if r < 0.0:
            r = -r

        Rin = self.get_inner_curve(z)
        if Rin == -2.0:
            return -1
        if Rin == 0.0:
            return 0
        if r <= Rin:
            return +1

        # could be inside the outer curve
        Rout = self.get_outer_curve(z)
        if Rout == -2.0:
            return -1
        if r <= Rout:
            return 0

        return -1

if __name__ == "__main__":

    cup = inner_cup("/home/beamuser/Documents/EGS/runEGS/cup_geometry/M03.json")

    shift = 78.78 - cup.Z2() # 100.78 - cup.Z2() # 136.78 - cup.Z2()

    for k in range(0, 1000):
        z = 1.0 * k
        y = cup.get_inner_curve(z)
        if y < 0.0:
            break

        print("   {0}   {1}".format(z + shift, y))

    z = cup.Z2()
    y = cup.get_outer_curve(z)
    print("   {0}   {1}".format(z + shift, y))
    # print(shift)
