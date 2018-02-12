# -*- coding: utf-8 -*-

import sys
import matplotlib.pyplot as plt
import struct

import numpy as np

"""
This is sample code to read .d3d kernel files.
After reading KDD file, code is computing KDD Scalar
"""


def expand_boundary(b):
    """
    Expand boundary vector around the left border in case it was symmetrized
    """
    n = b.shape[0]

    r = np.empty(n + n - 1, dtype = np.float32)

    i = 0
    for k in range(0, n):
        r[i] = -b[n-1-i]
        i += 1

    for k in range(0, n-1):
        r[i] = b[k+1]
        i += 1

    return r


def remake_boundary(f, n, sym):
    """
    Given filestream f and number of voxels/pixels n and symmetry flag sym,
    remake the boundary array
    """
    b = np.empty(n + 1, dtype = np.float32)

    for k in range(0, n + 1):
        b[k] = struct.unpack('f', f.read(4))[0]

    # uncoment if you prefer to work with full boundary
    #if sym is True:
    #    return expand_boundary(b)

    return b

def read_kdd(fname):
    """
    Given KDD filename, read KDD file and return back data tuple
    """
    with open(fname, "rb") as f:
        # read header, 32 bytes as 8*int32
        _ = struct.unpack('i', f.read(4))[0]
        _ = struct.unpack('i', f.read(4))[0]
        _ = struct.unpack('i', f.read(4))[0]
        _ = struct.unpack('i', f.read(4))[0]
        _ = struct.unpack('i', f.read(4))[0]
        _ = struct.unpack('i', f.read(4))[0]
        _ = struct.unpack('i', f.read(4))[0]
        _ = struct.unpack('i', f.read(4))[0]

        # read in the symmetry flags xsym, ysym, and zsym
        xsym = True if struct.unpack('i', f.read(4))[0] != 0 else False
        ysym = True if struct.unpack('i', f.read(4))[0] != 0 else False
        zsym = True if struct.unpack('i', f.read(4))[0] != 0 else False

        # read in dimensions nx, ny, and nz
        nx = struct.unpack('i', f.read(4))[0]
        ny = struct.unpack('i', f.read(4))[0]
        nz = struct.unpack('i', f.read(4))[0]

        # create boundary arrays, read in the boundaries
        xBoundary = remake_boundary(f, nx, xsym)
        yBoundary = remake_boundary(f, ny, ysym)
        zBoundary = remake_boundary(f, nz, zsym)

        #create dose matrix
        dose = np.empty((nx,ny,nz), dtype = np.float32)

        #read in the dose matrix, find max
        for i in range(0, nx):
            for j in range(0, ny):
                for k in range(0, nz):
                    dose[i, j, k] = struct.unpack('f',f.read(4))[0]
        try:
            _ = struct.unpack('i', f.read(4))[0]
            # if successfull, means we did something wrong, should be an exception thrown
            raise RuntimeError("There is something wrong with KDD file,  it's TOO LONG!")
        except struct.error as ex:
            # got and exception, file is ok, return good values
            pass

        return (xsym, ysym, zsym, nx, ny, nz, xBoundary, yBoundary, zBoundary, dose)

    return None

if __name__ == "__main__":

    import os

    # dirname = "D:/Ceres/Resource/PlanEngine/R5/Kdd"
    dirname = "D:/XCSW/XcDoseData/R3/PlanEngineResource/R3/Kdd"
    xsym25, ysym25, zsym25, nx25, ny25, nz25, xBoundary25, yBoundary25, zBoundary25, dose25 = read_kdd(os.path.join(dirname, "R3O0IQ00_Y000Z061C025.d3d"))
    idxmax25 = np.unravel_index(np.argmax(dose25, axis=None), dose25.shape)
    dmax25 = dose25[idxmax25]

    xsym15, ysym15, zsym15, nx15, ny15, nz15, xBoundary15, yBoundary15, zBoundary15, dose15 = read_kdd(os.path.join(dirname, "R3O0IQ00_Y000Z061C015.d3d"))
    idxmax15 = np.unravel_index(np.argmax(dose15, axis=None), dose15.shape)
    dmax15 = dose15[idxmax15]

    print("{0}  {1}  {2}  {3}  {4}  {5}".format(nx25, ny25, nz25, nx15, ny15, nz15))
    print("{0}  {1}  {2}  {3}  {4}  {5}".format(len(xBoundary25), len(yBoundary25), len(zBoundary25), len(xBoundary15), len(yBoundary15), len(zBoundary15)))

    f, (ax1,ax2) = plt.subplots(1,2, figsize=(12,7))

    img = ax1.imshow(dose15[0,:,:])
    ax1.set_title("QA kdd Z=61, C15")

    img = ax2.imshow(dose25[0,:,:])
    ax2.set_title("QA kdd Z=61, C25")

    f.subplots_adjust(right=0.8)
    cbar_ax = f.add_axes([0.85, 0.25, 0.05, 0.5])
    f.colorbar(img, cax=cbar_ax)

    QA15max = np.nanmax(dose15)
    QA25max = np.nanmax(dose25)
    print("Max C15 = {0}, {1}\nMax C25 = {2}, {3}\n".format(QA15max, dmax15, QA25max, dmax25))

    QA15Centroid = np.mean(dose15[0:1, 60:61, 52:53])
    QA25Centroid = np.mean(dose25[0:1, 60:61, 52:53])
    print("Centroid C15 = {0}\nCentroid C25 = {1}\n".format(QA15Centroid, QA25Centroid))

    aQA15CentroidAveraged = np.mean(dose15[0:1, 59:61, 51:53])
    aQA25CentroidAveraged = np.mean(dose25[0:1, 59:61, 51:53])
    print("Centroid averaged C15 = {0}\nCentroid averaged C25 = {1}".format(aQA15CentroidAveraged, aQA25CentroidAveraged))
    print("Centroid averaged C15 / Centroid averaged C25 = {0:1.4f}\n".format(aQA15CentroidAveraged/aQA25CentroidAveraged))

    bQA15CentroidAveraged = np.mean(dose15[0:1, 58:62, 50:54])
    bQA25CentroidAveraged = np.mean(dose25[0:1, 58:62, 50:54])
    print("Centroid averaged C15 = {0}\nCentroid averaged C25 = {1}".format(bQA15CentroidAveraged, bQA25CentroidAveraged))
    print("Centroid averaged C15 / Centroid averaged C25 = {0:1.4f}\n".format(bQA15CentroidAveraged/bQA25CentroidAveraged))

    cQA15CentroidAveraged = np.mean(dose15[0:1, 57:63, 49:55])
    cQA25CentroidAveraged = np.mean(dose25[0:1, 57:63, 49:55])
    print("Centroid averaged C15 = {0}\nCentroid averaged C25 = {1}".format(cQA15CentroidAveraged, cQA25CentroidAveraged))
    print("Centroid averaged C15 / Centroid averaged C25 = {0:1.4f}\n".format(cQA15CentroidAveraged/cQA25CentroidAveraged))

    print("Kdd scalar = {0:15.6e}   {1:15.6e}    {2:15.6e}    {3:15.6e}".format(1.0/cQA25CentroidAveraged, 1.0/bQA25CentroidAveraged, 1.0/aQA25CentroidAveraged, 1.0/QA25Centroid))

    plt.show()
