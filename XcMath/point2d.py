# -*- coding: utf-8 -*-
"""
Created on Thu May 14 19:29:28 2015

@author: Oleg.Krivosheev
"""

import numpy as np

class point2d:
    """
    2D point of two floats
    """
    
    def __init__(self, x = np.float32(0.0), y = np.float32(0.0)):
        """
        Constructor. Build point from x and y
        
        Parameters
        ----------
        
        x: float
            point X position
        y: float
            point Y position
        """
        
        self._x = np.float32( x )
        self._y = np.float32( y )
        
    def x(self):
        """
        returns: float
            point X position
        """
        return self._x
        
    def y(self):
        """
        returns: float
            point Y position
        """
        return self._y
