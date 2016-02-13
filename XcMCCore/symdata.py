# -*- coding: utf-8 -*-

import math
import numpy as np
import logging

from XcMCCore import phdata

class symdata(phdata.phdata):
    """
    phantom data which contains float-per-voxel together with dimensions,
    plus symmetrization flags and logic
    """

    EPS = 0.01 # in mm

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

        self._sym_x = False
        self._sym_y = False
        self._sym_z = False

        logging.info("symdata object constructed")

    def data(self):
        """
        Returns phantom data
        """
        return self._data

    def sym_x(self):
        """
        Returns X symmetry flag
        """
        return self._sym_x

    def sym_y(self):
        """
        Returns Y symmetry flag
        """
        return self._sym_y

    def sym_z(self):
        """
        Returns Z symmetry flag
        """
        return self._sym_z

    @staticmethod
    def could_sym(bounds, eps):
        """
        Check if bounds are symmetric so
        we could average by just summation
        :param bounds: array of bounds, n+1 in size
        :param eps: float, epsilon
        """

        n = len(bounds) - 1 # number of voxels
        for i in range(1, n):
            ileft_l = i - 1
            ileft_r = ileft_l + 1

            irght_l = n - i
            irght_r = irght_l + 1

            dleft = bounds[ileft_r] - bounds[ileft_l]
            drght = bounds[irght_r] - bounds[irght_l]

            delta = math.fabs(drght - dleft)
            if (delta > eps):
                return False

        # bins are equal within eps
        return True

    def could_sym_x(self):
        """
        True if could symmetrize X, False otherwise
        """
        return symdata.could_sym(self._bx, symdata.EPS)

    def could_sym_y(self):
        """
        True if could symmetrize Y, False otherwise
        """
        return symdata.could_sym(self._by, symdata.EPS)

    def could_sym_z(self):
        """
        True if could symmetrize Z, False otherwise
        """
        return symdata.could_sym(self._bz, symdata.EPS)

    def do_sym_x(self):
        """
        Make data symmetric over X
        """

        nx = self.nx()
        ny = self.ny()
        nz = self.nz()

        scale = np.float32(0.5)
        data  = np.empty((nx, ny, nz), dtype=np.float32)

        for iz in range(0, nz):
            for iy in range(0, ny):
                for ix in range(0, nx):
                    dleft = self._data[ix,      iy, iz]
                    drght = self._data[nx-1-ix, iy, iz]
                    data[ix,iy,iz] = (dleft + drght) * scale

        self._data  = data
        self._sym_x = True

    def do_sym_y(self):
        """
        Make data symmetric over Y
        """

        nx = self.nx()
        ny = self.ny()
        nz = self.nz()

        scale = np.float32(0.5)
        data  = np.empty((nx, ny, nz), dtype=np.float32)

        for iz in range(0, nz):
            for iy in range(0, ny):
                for ix in range(0, nx):
                    dleft = self._data[ix,      iy, iz]
                    drght = self._data[ix, ny-1-iy, iz]
                    data[ix,iy,iz] = (dleft + drght) * scale

        self._data  = data
        self._sym_y = True

    def do_sym_z(self):
        """
        Make data symmetric over Z
        """

        nx = self.nx()
        ny = self.ny()
        nz = self.nz()

        scale = np.float32(0.5)
        data  = np.empty((nx, ny, nz), dtype=np.float32)

        for iz in range(0, nz):
            for iy in range(0, ny):
                for ix in range(0, nx):
                    dleft = self._data[ix, iy,      iz]
                    drght = self._data[ix, iy, nz-1-iz]
                    data[ix,iy,iz] = (dleft + drght) * scale

        self._data  = data
        self._sym_z = True

