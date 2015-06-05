# -*- coding: utf-8 -*-

class collimator(object):
    """
    class represents particular collimator
    """
    
    def __init__(self, c):
        """
        Construct collimator taking its size, mm
        
        Parameters
        ----------
        
        c: integer
            collimator size
        """
        self._c = c
        
        if not self.invariant():
            raise ValueError("collimator", "negative value in constructor")
        
    def invariant(self):
        """
        Check class invariant
        
        returns: boolean
            True if good, False otherwise
        """
        
        if self._c < 0:
            return False
            
        return True
        
    def __eq__(self, other):
        """
        Checks equality of the collimators
        
        returns: boolean
            True if they are equal, False otherwise
        """
        return self._c == other._c
        
    def __ne__(self, other):
        """
        Checks inequality of the collimators
        
        returns: boolean
            True if they are NOT equal, False otherwise
        """
        return self._c != other._c
        
    def __lt__(self, other):
        """
        Ordering less than operator
        
        returns: boolean
            True if self is strictly less than other, False otherwise
        """        
        return self._c < other._c
        
    def __gt__(self, other):
        """
        Ordering greater than operator
        
        returns: boolean
            True if self is strictly greater than other, False otherwise
        """        
        return self._c > other._c

    def __str__(self):
        """
        Returns informal string representation of the collimator
        
        returns: string
            string representation of the collimator,
            for 25mm would be equal to C25
        """
        return "C{0}".format(self._c)
        
    def size(self):
        """
        Returns collimator size
        
        returns: float
            collimator size
        """
        return self._c
