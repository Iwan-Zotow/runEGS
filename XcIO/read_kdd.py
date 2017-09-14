# -*- coding: utf-8 -*-

import math
import struct

import numpy as np

def read_kdd(fname):
    """
    Read Kdd file and return back tuple
    """
    with open(fname, "rb") as f:
        # read header, 32 bytes
        _ = struct.unpack('i',f.read(4))[0]
        _ = struct.unpack('i',f.read(4))[0]
        _ = struct.unpack('i',f.read(4))[0]
        _ = struct.unpack('i',f.read(4))[0]
        _ = struct.unpack('i',f.read(4))[0]
        _ = struct.unpack('i',f.read(4))[0]
        _ = struct.unpack('i',f.read(4))[0]
        _ = struct.unpack('i',f.read(4))[0]

        # read in the xsym, ysym, and zsym
        xsym = struct.unpack('i',f.read(4))[0]
        ysym = struct.unpack('i',f.read(4))[0]
        zsym = struct.unpack('i',f.read(4))[0]
        print(xsym)
        print(ysym)
        print(zsym)

        # read in nx, ny, and nz
        nx = struct.unpack('i',f.read(4))[0]
        ny = struct.unpack('i',f.read(4))[0]
        nz = struct.unpack('i',f.read(4))[0]
        print(nx)
        print(ny)
        print(nz)

        # create boundary lists
        xBoundary = np.empty(nx + 1, dtype = np.float32)
        yBoundary = np.empty(ny + 1, dtype = np.float32)
        zBoundary = np.empty(nz + 1, dtype = np.float32)

        #read in the boundaries
        for k in range(0, nx+1):
            xBoundary[k] = struct.unpack('f',f.read(4))[0]

        for k in range(0, ny+1):
            yBoundary[k] = struct.unpack('f',f.read(4))[0]

        for к in range(0, nz+1):
            zBoundary[к] = struct.unpack('f',f.read(4))[0]

        #create dose matrix
        dose = np.empty((nx,ny,nz), dtype = np.float32)

        #read in the dose matrix, find max
        dmax = -1.0
        for i in range(0, nx):
            for j in range(0, ny):
                for k in range(0, nz):
                    v = struct.unpack('f',f.read(4))[0]
                    dose[i, j, k] = v
                    if v > dmax:
                        dmax = v

        return (xsym, ysym, zsym, nx, ny, nz, xBoundary, yBoundary, zBoundary, dose, dmax)

    return None

if __name__ == "__main__":
    import sys

    print(sys.argv[0])
    fname = sys.argv[1]

    xsym, ysym, zsym, nx, ny, nz, xBoundary, yBoundary, zBoundary, dose, dmax = read_kdd(fname)

    print(dmax)
