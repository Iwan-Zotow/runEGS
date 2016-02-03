#!/usr/bin/env python

import sys

X = 0 # coordinate index
D = 1 # dose index

F =  0 # first
L = -1 # last

class cspline(object):
    """
    cubic spline class, data required to be in ascending X order
    """

    def __init__( self, pts ):
        """
        constructor, takes array of points as an argument
        """

        self._pts  = pts

        self._xmin = self._pts[F][X]
        self._xmax = self._pts[L][X]

        if self._xmin >= self._xmax:
            raise ValueError("Error in cspline constructor, min/max {0} {1} ".format(self._xmin, self._xmax))

        lpts = len(self._pts)
        for i in range( 1, lpts ):
            if self._pts[i] <= self._pts[i-1]:
                raise ValueError("Non monotonic input data detected in cspline: index {0}".format(i))

        self.slope_ = []
        self.calc_slope()

    def calc_slope( self ):
        """
        calculate slope parameters
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

            self.slope_.append( 2.0 * a * self._pts[i][X] + b )

    def find_bin( self, x ):
        """
        given X value, find spline bin using binary search
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

    def calc_data( self, x ):
        """
        given X value, returns computed Y value
        using precomputed cubic spline coefficients
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

        sl = self.slope_

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

    def __len__( self ):
        return len( self._pts )

if __name__ == "__main__":

    import sys

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
            y = cs.calc_data( x )
            print("{0}  {1} {2} ".format(i, x, y))
        except ValueError:
            pass

    sys.exit(0)
