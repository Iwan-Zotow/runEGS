
# -*- coding: utf-8 -*-
import utils
import logging

class cupint(object):
    """
    Interpolation of the cup curve from cup CAD drawings data

    Given the cup data from drawings, produce computed (r, z) curve
    """

    def __init__( self, cup, zshift ):
        """
        Construct interpolator from the cup and zshift

        Parameters
        ----------

        cup: inner_cup
            inner cup object

        zshift: double
            inner cup Z shift, mm
        """

        self._cup    = cup
        self._zshift = zshift

        if not self.invariant():
            raise RuntimeError("cupint", "from constructor")

        self._zmin = 0.0
        self._zmax = self._cup.zmax_outer() + zshift

        # compute gradient at the cup edge for outer extrapolation
        za = self._cup.zmin_outer()
        zb = za + 0.5
        va = self._cup.get_outer_curve(za)
        vb = self._cup.get_outer_curve(zb)

        self._grad = (vb - va) / (zb - za)

        # done wih computing, now logging
        logging.info("cupint constructed")
        logging.debug(str(cup))
        logging.debug(str(zshift))
        logging.debug(self._grad)

    def invariant(self):
        """
        Checks validity of the input

        returns: boolean
            True if ok, False otherwise
        """

        if self._cup == None:
            return False

        if self._cup.invariant() == False:
            return False

        # shall be descending
        # ...

        return True

    def zmin(self):
        """
        Returns interpolator abscissa minimum, mm
        """
        return self._zmin

    def zmax(self):
        """
        Returns interpolator abscissa maximum, mm
        """
        return self._zmax

    def interpolate(self, z):
        """
        Interpolate value from curve having index of the bin and abscissa value

        Parameters
        ----------

        z: float
            abscissa value

        returns: float
            interpolated value
        """

        logging.debug(str(z))

        # below zmin
        # print("Interpolate {0} {1}".format(z, self._zmin))
        if (z < self._zmin):
            raise RuntimeError("cupint::interpolate", "z less than zmin")

        # above zmax
        if z > self._zmax:
            raise RuntimeError("cupint::interpolate", "z greate than zmax")

        if z <= self._zshift: # here use gradient
            return self._cup.get_outer_curve(0.0) + self._grad*(z - self._zshift)

        return self._cup.get_outer_curve( utils.clamp(z - self._zshift, self._cup.zmin_outer(), self._cup.zmax_outer() ) )

    def extrapolate(self, z):
        """
        Extrapolate value from curve having index of the bin and abscissa value

        Parameters
        ----------

        z: float
            abscissa value

        returns: float
            extrapolated value
        """
        logging.debug(str(z))

        if z > self._zmax:
            return 0.0

        if z < self._zmin:
            return self.interpolate(0.0)

        return self.interpolate(z)

if __name__ == "__main__":
    print("QQQ")
