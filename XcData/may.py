import os
import math
import struct

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from mayavi import mlab
from mayavi.mlab import *

filePath = "/home/kriol/data/R8O1IS01C25_Y0Z55/R8O1IS01C25_Y0Z55.3ddose"

f = open(filePath,'r')

#read in the dimensions
line = f.readline();
lineSplit = line.split(" ")
lineSplit = [x for x in lineSplit if x]  # remove empty lines


nx = int(lineSplit[0])
ny = int(lineSplit[1])
nz = int(lineSplit[2])
print nx,ny,nz

#read in nx, ny, and nz
#nx = struct.unpack('i',f.read(4))[0]
line = f.readline()
line = f.readline()
line = f.readline()

#create boundary lists
xBoundary = []
yBoundary = []
zBoundary = []

#create dose matrix

dose = np.empty((nx,ny,nz))

line = f.readline()
split = line.split(" ")
split = [x for x in split if x]  # remove empty lines

k = 0
for iz in range(0, nz):
    for iy in range(0, ny):
        for ix in range(0, nx):
            dose[ix,iy,iz] = float(split[k])
            k += 1

#Plot part in IPython

x,y,z=np.ogrid[1:nx:1,1:ny:1, 1:nz:1]

print(dose.ptp())

src = mlab.pipeline.scalar_field(dose)
mlab.pipeline.iso_surface(src, contours=[dose.min()+0.1*dose.ptp(), ], opacity=0.3)
mlab.pipeline.iso_surface(src, contours=[dose.max()-0.1*dose.ptp(), ], opacity=0.3)
mlab.pipeline.iso_surface(src, contours=[dose.max()-0.2*dose.ptp(), ], opacity=0.3)
mlab.pipeline.iso_surface(src, contours=[dose.max()-0.3*dose.ptp(), ], opacity=0.3)
#contour3d(src)
mlab.show()
