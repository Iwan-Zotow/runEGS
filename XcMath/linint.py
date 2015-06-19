# -*- coding: utf-8 -*-

import numpy as np
import logging

class linint(object):
    """
    Given the curve, produce linearly interpolated values
    """
    
    def __init__( self, points ):
        """
        Construct interpolator from the curve
        
        Parameters
        ----------
        points: array of points
            arrays of 2D points
        """
        
        # make copy of points
        self._points = points[:]
        
        if not self.invariant():
            raise RuntimeError("linint", "invariant is broken in constructor")
        
        self._len = len(points)
        
        self._zmin = self._points[-1].x()
        self._zmax = self._points[0].x()
        
        if not self.invariant():
            raise RuntimeError("linint", "from constructor")
        
        logging.info("linint constructed")
        logging.debug(str(points))
        
    def invariant(self):
        """
        Checks validity of the input
        
        returns: boolean
            True if ok, False otherwise
        """

        if self._points == None:
            return False

        if len(self._points) <= 1:
            return False
            
        # shall be descending
        prev = np.float32(1000000.0)
        for p in self._points:
            z = p.x()
            if z > prev:
                return False
            if z == prev:
                return False
            prev = z
            
        return True
        
    def __len__(self):
        """
        Length        
        
        returns: integer
            length
        """
        return self._len

    def __getitem__(self, idx):
        """
        Indexing operator
        
        Parameters
        ----------

        idx: integer
            point index
        
        returns: point
            2D point at given index
        """
        logging.debug(str(idx))        
        
        if idx < 0:
            raise ValueError("linint", "index is negative")
        
        if idx >= self._len:
            raise ValueError("linint", "index is too large")
            
        return self._points[idx]
        
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
#        print(self._points[idx].x())
#        print(self._points[idx+1].x())
#        print(idx)

        # above zmax        
        if (idx == -1):
            raise RuntimeError("interpolate", "index is -1")
            
        # below zmin
        if (idx == -2):
            raise RuntimeError("interpolate", "index is -2")
        
        p = (z - self._points[idx+1].x()) / (self._points[idx].x() - self._points[idx+1].x())
        q = 1.0 - p
        
#        print(p)
#        print(q)
#        print(self._points[idx].y())
#        print(self._points[idx+1].y())
        
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

    
