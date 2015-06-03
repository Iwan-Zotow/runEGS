# -*- coding: utf-8 -*-
"""
Created on Wed May 06 15:14:24 2015

@author: Oleg.Krivosheev
"""

import numpy as np
import logging

import phandim

class phantom(phandim.phandim):
    """
    phantom which contains data together with dimensions
    """
    
    def __init__(self, bx, by, bz):
        """
        Phantom
        """
        super(self.__class__, self).__init__(bx, by, bz)
        
        # material index
        self._data = np.empty((self.nx(), self.ny(), self.nz()), dtype=np.uint8)
        
        # density
        self._dens = np.empty((self.nx(), self.ny(), self.nz()), dtype=np.float32)
        
        logging.info("phantom object constructed")
        
    def data(self):
        """
        Returns phantom data
        """

        return self._data

    def dens(self):
        """
        Returns phantom data
        """

        return self._dens
