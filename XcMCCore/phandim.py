# -*- coding: utf-8 -*-

import logging
import numpy as np

class phandim(object):
    """
    class to hold phantom dimensions
    """

    def __init__(self, bx, by, bz):
        """
        Constructor. Builds object from boundary vectors
        
        Parameters
        ----------
        
        bx: array of floats
            voxel boundaries in X, mm
            
        by: array of floats
            voxel boundaries in Y, mm
        
        bz: array of floats
            voxel boundaries in Z, mm
        """
        if bx == None:
            raise RuntimeError("phantom", "Null bx parameter in constructor")            
        if len(bx) < 2:
            raise RuntimeError("phantom", "bx is too short in constructor")

        if by == None:
            raise RuntimeError("phantom", "Null by parameter in constructor")        
        if len(by) < 2:
            raise RuntimeError("phantom", "by is too short in constructor")

        if bz == None:
            raise RuntimeError("phantom", "Null bz parameter in constructor")                    
        if len(bz) < 2:
            raise RuntimeError("phantom", "bz is too short in constructor")
        
        self._bx = phandim.copy_boundary_array(bx)
        self._by = phandim.copy_boundary_array(by)
        self._bz = phandim.copy_boundary_array(bz)
        
        logging.info("phandim initialized")
        logging.debug(str(bx))
        logging.debug(str(by))
        logging.debug(str(bz))
        
    @staticmethod
    def copy_boundary_array(b):
        """
        allocate NP array and copy content into it
        
        Parameters
        ----------
        
        b: array of floats
            input vector of boundaries, mm
            
        returns:
            sorted NP array of boundaries
        """
        bnp = np.empty(len(b), dtype=np.float32)
        for k in range(0, len(b)):
            bnp[k] = np.float32( b[k] )
            
        # just in case, sort boundaries
        bnp = np.sort(bnp)

        return bnp
        
    @staticmethod
    def check_sorted(b):
        """
        Check if array is sorted in ascending order without dups
        
        Parameters
        ----------

        b: array
            boundaries
            
        returns: boolean
            True if sorted, False otherwise
        """
        for k in range(1,len(b)):
            if b[k] == b[k-1]:
                return False
            if b[k] < b[k-1]:
                return False
                
        return True
        
    def bx(self):
        """
        Return X boundaries        
            
        returns: array
            X boundaries
        """
        return self._bx
        
    def by(self):
        """
        Return Y boundaries        
            
        returns: array
            Y boundaries
        """
        return self._by
        
    def bz(self):
        """
        Return Z boundaries        
            
        returns: array
            Z boundaries
        """
        return self._bz
        
    def nx(self):
        """
        Returns number of voxels in X
        
        returns: integer
            number of X voxels
        """
        return len(self._bx)-1
        
    def ny(self):
        """
        Returns number of voxels in Y

        returns: integer
            number of Y voxels
        """
        return len(self._by)-1

    def nz(self):
        """
        Returns number of voxels

        returns: integer
            number of Z voxels
        """
        return len(self._bz)-1

