# -*- coding: utf-8 -*-

import numpy as np
import logging

from XcMCCore import phandim

class phdata(phandim.phandim):
    """
    phantom data which contains float-per-voxel together with dimensions
    """

    def __init__(self, bx, by, bz):
        """
        Phantom data constructor

        Parameters
        ----------

        bx: array of floats
            voxel boundaries in X, mm

        by: array of floats
            voxel boundaries in Y, mm

        bz: array of floats
            voxel boundaries in Z, mm
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

    def find_max(self):
        """
        Find data maximum value,
        returns position and the value
        """

        dmax = np.float32(-99999999.0)
        xmax = -1
        ymax = -1
        zmax = -1
        for iz in range(0, nz):
            for iy in range(0, ny):
                for ix in range(0, nx):

                    d = self._data[ix,iy,iz]
                    if d > dmax:
                        dmax = d
                        xmax = ix
                        ymax = iy
                        zmax = iz

        return (xmax, ymax, zmax, dmax)

