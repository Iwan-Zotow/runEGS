# -*- coding: utf-8 -*-

import numpy as np
import logging

import phdata

class derrdata(phdata.phdata):
    """
    dose&error data,
    which contains float-per-voxel dose plus float-per-voxel error
    """
    
    def __init__(self, bx, by, bz):
        """
        Sym data constructor
        
        Parameters
        ----------
        
        bx: array of floats
            voxel boundaries in X, mm
            
        by: array of floats
            voxel boundaries in Y, mm
        
        bz: array of floats
            voxel boundaries in Z, mm       
        """

        super(symdata, self).__init__(bx, by, bz)

        self._error = np.empty((self.nx(), self.ny(), self.nz()), dtype=np.float32)
        
        logging.info("derrdata object constructed")
                        
    def error(self):
        """
        Returns error arrray
        """

        return self._error

