# -*- coding: utf-8 -*-

import numpy as np
import logging

import phandim

class phdata(phandim.phandim):
    """
    phantom data which contains float-per-voxel together with dimensions
    """
    
    def __init__(self, bx, by, bz):
        """
        Phantom data constructor
        """

        super(phdata, self).__init__(bx, by, bz)
        
        # one float value per voxel
        self._data = np.empty((self.nx(), self.ny(), self.nz()), dtype=np.float32)
        
        logging.info("phdata object constructed")        
        
    def data(self):
        """
        Returns phantom data
        """

        return self._data

