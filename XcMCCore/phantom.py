# -*- coding: utf-8 -*-

import numpy as np
import logging

import phdata

class phantom(phdata.phdata):
    """
    phantom which contains data together with dimensions
    """
    
    def __init__(self, bx, by, bz):
        """
        Phantom constructor
        
        Parameters
        ----------
        
        bx: array of floats
            voxel boundaries in X, mm
            
        by: array of floats
            voxel boundaries in Y, mm
        
        bz: array of floats
            voxel boundaries in Z, mm
        """

        super(phantom, self).__init__(bx, by, bz)
        
        # material index
        self._mats = np.empty((self.nx(), self.ny(), self.nz()), dtype=np.uint8)        
        
        logging.info("phantom object constructed")        
        
    def mats(self):
        """
        Returns phantom materials
        """

        return self._mats

