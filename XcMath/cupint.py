# -*- coding: utf-8 -*-

import numpy as np
import logging

class cupint(object):
    """
    Given the cup equation, produce computed
    """
    
    def __init__( self, cup, zshift ):
        """
        Construct interpolator from the cup and zshift
        
        Parameters
        ----------
        
        cup: inner_cup
            inner cup object
            
        zshift:
            inner cup Z shift, mm            
        """
        
        self._cup    = cup
        self._zshift = zhift
        
        if not self.invariant():
            raise RuntimeError("cupint", "from constructor")
        self._zmin = self._cup.D1() - zshift
        self._zmax = self._cup.D2() - zshift
        
        logging.info("cupint constructed")
        logging.debug(str(cup))
        logging.debug(str(zshift))
        
    def invariant(self):
        """
        Checks validity of the input
        
        returns: boolean
            True if ok, False otherwise
        """

        if self._cup == None:
            return False

        # shall be descending
        # ...
            
        return True
        
    def __len__(self):
        """
        Length        
        
        returns: integer
            length
        """
        return 10000

    def zmin(self):
        """
        Returns interpolator abscissa minimum
        """
        return self._zmin
        
    def zmax(self):
        """
        Returns interpolator abscissa maximum
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

        idx = self.find_idx(z)
        # print(self._points[idx].x())
        # print(self._points[idx+1].x())
        # print(idx)

        # above zmax        
        if (idx == -1):
            raise RuntimeError("interpolate", "index is -1")
            
        # below zmin
        if (idx == -2):
            raise RuntimeError("interpolate", "index is -2")
        
        p = (z - self._points[idx+1].x()) / (self._points[idx].x() - self._points[idx+1].x())
        q = 1.0 - p
        
        # print(p)
        # print(q)
        # print(self._points[idx].y())
        # print(self._points[idx+1].y())
        
        return p * self._points[idx].y() + q * self._points[idx+1].y()

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
        
        if z >= self._zmin:
            return self.interpolate(z)

        idx = self._len - 1
        
        p = (z - self._points[idx].x()) / (self._points[idx-1].x() - self._points[idx].x())
        q = 1.0 - p
        
        return p * self._points[idx-1].y() + q * self._points[idx].y()

    def find_idx(self, z):
        """
        Given z, find index
        
        Parameters
        ----------

        z: float
            abscissa value
        
        returns: integer
            index of the bin
        """
        logging.debug(str(z))     
        
        if z > self._zmax:
            return -1
        
        if z < self._zmin:
            return -2

        lo = self._len-1
        hi = 0            
        while True:
            me = (lo + hi) // 2
            xx = self._points[me].x()
            if xx > z:
                hi = me
            else:
                lo = me
                
            if lo - hi == 1:
                break
            
        return hi

if __name__ == "__main__":
    
    import point2d    
    
    curve = []
    curve.append(point2d.point2d(5.0, 1.0))
    curve.append(point2d.point2d(4.0, 2.0))
    curve.append(point2d.point2d(3.0, 3.0))
    curve.append(point2d.point2d(2.0, 4.0))
    curve.append(point2d.point2d(1.0, 5.0))
    
    li = linint(curve)
    v  = li.extrapolate(0.1)
    
    print(v)

    
