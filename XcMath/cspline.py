# -*- coding: utf-8 -*-

import copy

X = 0 # coordinate index
D = 1 # data index

F =  0 # first idx
L = -1 # last  idx

class cspline(object):
    """
    Cubic spline class,
    data could be in any order, but sorted, internally would be
    in the ascending X order
    """

    def __init__( self, pts ):
        """
        Spline constructor

        Parameters
        ----------

        pts: array
            array of points as an argument
        """

        self._pts  = copy.deepcopy(pts)

        self._xmin = self._pts[F][X]
        self._xmax = self._pts[L][X]

        if self._xmin >= self._xmax:
            # revert array
            self._pts.reverse()
            print(self._pts)

            self._xmin = self._pts[F][X]
            self._xmax = self._pts[L][X]

        lpts = len(self._pts)
        for i in range( 1, lpts ):
            if self._pts[i] <= self._pts[i-1]:
                raise ValueError("Non monotonic input data detected in cspline: index {0}".format(i))

        self._slope = []
        self.calc_slope()

    def calc_slope( self ):
        """
        Calculate spline slope parameters

        Parameters
        ----------

        self: cspline
            this
        """

        lpts = len(self._pts)
        for i in range( 0, lpts ):

            l = 0
            if i == lpts-1:
                l = i - 2
            elif i > 0:
                l = i - 1

            p  = self._pts[l]
            x1 = p[X]
            y1 = p[D]

            p  = self._pts[l+1]
            x2 = p[X]
            y2 = p[D]

            p  = self._pts[l+2]
            x3 = p[X]
            y3 = p[D]

            a1 = ( x1*x1 - x3*x3 )
            a2 = ( x2*x2 - x3*x3 )

            b1 = x1 - x3
            b2 = x2 - x3

            c1 = y1 - y3
            c2 = y2 - y3
            d  = a1 * b2 - a2 * b1

            a  = (c1 * b2 - c2 * b1)/d
            b  = (a1 * c2 - a2 * c1)/d

            self._slope.append( 2.0 * a * self._pts[i][X] + b )

    def find_bin( self, x ):
        """
        Given X value, find spline bin using binary search

        Parameters
        ----------

        self: cspline
            this

        x: double
            point where to find bin

        returns: int
            bin index
        """
        lo = 0
        hi = len(self._pts) - 1
        while 1:
            me = int( ( lo + hi ) / 2 )
            px = self._pts[me][X]
            if x == px:
                return me
            if x > px:
                lo = me
            else:
                hi = me

            if hi - lo <= 1:
                return lo

    def calculate( self, x ):
        """
        Given X value, returns computed Y value
        using precomputed cubic spline coefficients

        Parameters
        ----------

        self: cspline
            this

        x: double
            point where to find bin

        returns: double
            computed value
        """
        if ( x > self._xmax ):
            raise ValueError("cspline: More than max {0} ({1} {2})".format(x, self._xmin, self._xmax))

        if ( x < self._xmin ):
            raise ValueError("cspline: Less than min {0} ({1} {2})".format(x,self._xmin,self._xmax))

        if ( x == self._xmin ):
            return self._pts[F][D]

        if ( x == self._xmax ):
            return self._pts[L][D]

        l = self.find_bin( x )

        pl = self._pts[l]
        pn = self._pts[l+1]

        sl = self._slope

        c  = 1.0/( pn[X] - pl[X] )
        x1 = x - pl[X]
        x2 = x - pn[X]

        y  = pl[D] * c*c * x2*x2 * (1.0 + 2.0 * c * x1) + pn[D] * c*c * x1*x1 * ( 1.0 - 2.0 * c * x2) + sl[l] * c*c * x2*x2 * x1 + sl[l+1] * c*c * x1*x1 * x2

        return y

    def xmin( self ):
        return self._xmin

    def xmax( self ):
        return self._xmax

    def pts( self ):
        return self._pts

    def slope( self ):
        return self._slope

    def __len__( self ):
        return len( self._pts )

    def invariant(self):
        """
        Self consistency check

        Parameters
        ----------

        self: cspline
            this

        returns: boolean
            True on ok, False otherwise
        """

        if self._pts == None:
            return False

        if self._slope == None:
            return False

        if self._xmin >= self._xmax:
            return False

        if len(self._pts) <= 3:
            return False

        return True

if __name__ == "__main__":

    import sys
    import math
    import random

    def linear_test():
        pts = []
        for i in range(0, 10):
            x = float(i)
            y = float(10 - i)

            print("  {0} {1} ".format(x, y))

            pts.append( (x, y) )

        print(" ")

        cs = cspline( pts )

        for i in range(0, 11):
            x = float(i) - 0.5
            try:
                y = cs.calculate( x )
                print("{0}  {1} {2}".format(i, x, y))
            except ValueError as e:
                print("Exception: {0}  {1}".format(x, y))
                print("Exception: " + str(e))
                print(" ")

    def sinus_test(n):
        pts = []
        for i in range(0, n+1):
            x = float(i)/float(n) * (math.pi/2.0)
            y = math.sin(x)

            print("  {0} {1} ".format(x, y))

            pts.append( (x, y) )

        print(" ")

        cs = cspline( pts )

        for i in range(0, 3*n+1):
            x = 0.0 + (math.pi/2.0)*random.random()
            try:
                y = cs.calculate( x )
                print("{0}  {1}".format(x, y))
            except ValueError as e:
                print("Exception: {0}  {1}".format(x, y))
                print("Exception: " + str(e))

    def invsinus_test(n):
        pts = []
        for i in range(0, n+1):
            x = float(n-i)/float(n) * (math.pi/2.0)
            y = math.sin(x)

            print("  {0} {1} ".format(x, y))

            pts.append( (x, y) )

        print(" ")

        cs = cspline( pts )

        for i in range(0, 3*n+1):
            x = 0.0 + (math.pi/2.0)*random.random()
            try:
                y = cs.calculate( x )
                print("{0}  {1}".format(x, y))
            except ValueError as e:
                print("Exception: {0}  {1}".format(x, y))
                print("Exception: " + str(e))

#    linear_test()

#    sinus_test(10)

    invsinus_test(20)

    sys.exit(0)
