# -*- coding: utf-8 -*-
"""
Created on Fri May 08 16:59:23 2015

@author: Oleg.Krivosheev
"""

import numpy as np

class collimator:
    """
    class represents particular collimator
    """
    
    def __init__(self, c):
        """
        Construct collimator taking its size, mm
        """
        self._c = c
        
    def __eq__(self, other):
        """
        Checks equality of the collimators
        :returns: true if they are equal, false otherwise
        """
        return self._c == other._c
        
    def __ne__(self, other):
        """
        Checks inequality of the collimators
        :returns: true if they are not equal, false otherwise
        """
        return self._c != other._c
        
    def __le__(self, other):
        """
        Ordering less than operator 
        :returns: true if self is smaller, false otherwise
        """        
        return self._c < other._c
        
    def __gr__(self, other):
        """
        Ordering greater than operator 
        :returns: true if self is greater, false otherwise
        """        
        return self._c > other._c

    def __str__(self):
        """
        Returns informal string representation of the collimator
        """
        cc = np.int32(self._c)
        return "C{0:0>d2}".format(cc) # shall I add letter C in front?
        
    def size(self):
        """
        """
        return self._c
