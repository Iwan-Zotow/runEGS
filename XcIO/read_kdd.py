# -*- coding: utf-8 -*-

import math
import matplotlib.pyplot as plt
import struct

import numpy as np

def read_kdd(fname):
    """
    Read Kdd file and return back tuple


    """
    with open(fname, "rb") as f:
        # read header, 32 bytes
        _ = struct.unpack('i', f.read(4))[0]
        _ = struct.unpack('i', f.read(4))[0]
        _ = struct.unpack('i', f.read(4))[0]
        _ = struct.unpack('i', f.read(4))[0]
        _ = struct.unpack('i', f.read(4))[0]
        _ = struct.unpack('i', f.read(4))[0]
        _ = struct.unpack('i', f.read(4))[0]
        _ = struct.unpack('i', f.read(4))[0]

        # read in the symmetry flags xsym, ysym, and zsym
        xsym = struct.unpack('i', f.read(4))[0]
        ysym = struct.unpack('i', f.read(4))[0]
        zsym = struct.unpack('i', f.read(4))[0]

        # read in dimensions nx, ny, and nz
        nx = struct.unpack('i', f.read(4))[0]
        ny = struct.unpack('i', f.read(4))[0]
        nz = struct.unpack('i', f.read(4))[0]

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

    import os

    dirname = "D:/Ceres/Resource/PlanEngine/XcDoseData/trunk/PlanEngineResource/R8/Kdd"

    xsym25, ysym25, zsym25, nx25, ny25, nz25, xBoundary25, yBoundary25, zBoundary25, dose25, dmax25 = read_kdd(os.path.join(dirname, "R8O0IQ00_Y000Z061C025.d3d"))
    xsym15, ysym15, zsym15, nx15, ny15, nz15, xBoundary15, yBoundary15, zBoundary15, dose15, dmax15 = read_kdd(os.path.join(dirname, "R8O0IQ00_Y000Z061C015.d3d"))

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

    QA15Centroid = np.mean(dose15[0:1, 59:60, 52:53])
    QA25Centroid = np.mean(dose25[0:1, 59:60, 52:53])
    print("Centroid C15 = {0}\nCentroid C25 = {1}\n".format(QA15Centroid, QA25Centroid))

    aQA15CentroidAveraged = np.mean(dose15[0:1, 59:61, 52:54])
    aQA25CentroidAveraged = np.mean(dose25[0:1, 59:61, 52:54])
    print("Centroid averaged C15 = {0}\nCentroid averaged C25 = {1}".format(aQA15CentroidAveraged, aQA25CentroidAveraged))
    print("Centroid averaged C15 / Centroid averaged C25 = {0:1.4f}\n".format(aQA15CentroidAveraged/aQA25CentroidAveraged))

    bQA15CentroidAveraged = np.mean(dose15[0:1, 58:62, 51:55])
    bQA25CentroidAveraged = np.mean(dose25[0:1, 58:62, 51:55])
    print("Centroid averaged C15 = {0}\nCentroid averaged C25 = {1}".format(bQA15CentroidAveraged, bQA25CentroidAveraged))
    print("Centroid averaged C15 / Centroid averaged C25 = {0:1.4f}\n".format(bQA15CentroidAveraged/bQA25CentroidAveraged))

    cQA15CentroidAveraged = np.mean(dose15[0:1, 57:63, 50:56])
    cQA25CentroidAveraged = np.mean(dose25[0:1, 57:63, 50:56])
    print("Centroid averaged C15 = {0}\nCentroid averaged C25 = {1}".format(cQA15CentroidAveraged, cQA25CentroidAveraged))
    print("Centroid averaged C15 / Centroid averaged C25 = {0:1.4f}\n".format(cQA15CentroidAveraged/cQA25CentroidAveraged))

    print("Kdd scalar = {0:15.6e}   {1:15.6e}    {2:15.6e}    {3:15.6e}".format(1.0/cQA25CentroidAveraged, 1.0/bQA25CentroidAveraged, 1.0/aQA25CentroidAveraged, 1.0/QA25Centroid))

    plt.show()
