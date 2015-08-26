#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import struct
import numpy as np
import os
import sys
from matplotlib.colors import colorConverter
import matplotlib.pyplot as plt

from Convert3ddoseToD3d import *

def Read3ddose(filePath):
    with open(filePath, 'r') as f:    
        #read in the dimensions
        line = f.readline()
        (nx, ny, nz) = get_dimensions(line)
        print(nx, ny, nz)    
        line = f.readline()
        bx = get_boundaries(nx, line)
        print(bx)    
        line = f.readline()
        by = get_boundaries(ny, line)
        print(by)    
        line = f.readline();
        bz = get_boundaries(nz, line)
        print(bz)    
        #create dose matrix    
        line = f.readline()
        dose3ddose = get_3ddata(nx, ny, nz, line)
        return [dose3ddose,nx,ny,nz,bx,by,bz]

def main():

    filePathShortSteel = "old/R8O3IL08C25_Y40Z30.3ddose"
    filePathLongSteel  = "new/R8O3IL08C25_Y40Z30.3ddose"

    [doseL,nxL,nyL,nzL,xbL,ybL,zbL] = Read3ddose(filePathLongSteel)
    [doseS,nxS,nyS,nzS,xbS,ybS,zbS] = Read3ddose(filePathShortSteel)
    
    doseL = averageX_3ddata(nxL,nyL,nzL, doseL, 0.5)

    doseS = averageX_3ddata(nxS,nyS,nzS, doseS, 0.5)
        
    # summing over 4 lines around 0 for a profile 
    profL = 0.25*(doseL[36,:,40] + doseL[36,:,41] + doseL[37,:,40] + doseL[37,:,41])  
    profS = 0.25*(doseS[36,:,40] + doseS[36,:,41] + doseS[37,:,40] + doseS[37,:,41])
    
    topL = np.mean(profL[31:42])
    topS = np.mean(profS[31:42])
    
    profS = profS[:]*1.7383714984342543/1.2919502147722337 #topL/topS # so short and long are normalized in the same way
    
    print(topL, topS, np.mean(profS[31:42]))

    fig1 = plt.figure(1)

    ax = fig1.gca()

    ax.plot(profS,'b')
    ax.plot(profL,'r')

    plt.show()

if __name__ == "__main__":
    main()

