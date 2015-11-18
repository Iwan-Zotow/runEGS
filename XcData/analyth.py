#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import math
import struct

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import colorConverter

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

    top = "/home/beamuser/Documents/EGS/runEGS/R8O3IL08"
    clm = "C25"

    file_std = os.path.join(top, clm, "std.3ddose")
    file_dbl = "/home/beamuser/Documents/EGS/runEGS/R8O3IL08/R8O3IL08C25_Y0Z0/R8O3IL08C25_Y0Z0.3ddose" # os.path.join(top, clm, "dblstat.3ddose")
    file_phs = os.path.join(top, clm, "dblphsf.3ddose")
    file_rnd = os.path.join(top, clm, "dblphsfrand.3ddose")

    [dose_std, nx_std, ny_std, nz_std, xb_std, yb_std, zb_std] = Read3ddose(file_std)
    [dose_dbl, nx_dbl, ny_dbl, nz_dbl, xb_dbl, yb_dbl, zb_dbl] = Read3ddose(file_dbl)
    [dose_phs, nx_phs, ny_phs, nz_phs, xb_phs, yb_phs, zb_phs] = Read3ddose(file_phs)
    [dose_rnd, nx_rnd, ny_rnd, nz_rnd, xb_rnd, yb_rnd, zb_rnd] = Read3ddose(file_rnd)

    dose_std = averageX_3ddata(nx_std, ny_std, nz_std, dose_std, 0.5)
    dose_dbl = averageX_3ddata(nx_dbl, ny_dbl, nz_dbl, dose_dbl, 0.5)
    dose_phs = averageX_3ddata(nx_phs, ny_phs, nz_phs, dose_phs, 0.5)
    dose_rnd = averageX_3ddata(nx_rnd, ny_rnd, nz_rnd, dose_rnd, 0.5)
        
    # summing over 4 lines around 0 for a profile 
    #prof_std = 0.25*(dose_std[36,:,40] + dose_std[36,:,41] + dose_std[37,:,40] + dose_std[37,:,41])  
    #prof_dbl = 0.25*(dose_dbl[36,:,40] + dose_dbl[36,:,41] + dose_dbl[37,:,40] + dose_dbl[37,:,41])
    
    prof_std = dose_std[36,:,40]
    prof_dbl = dose_dbl[36,:,40]
    prof_phs = dose_phs[36,:,40]
    prof_rnd = 2.0*dose_rnd[36,:,40]
    
    #prof_std = prof_std[:]*1.0/1.0 # so short and long are normalized in the same way
    #top_std = np.mean(prof_std[31:42])
    #top_dbl = np.mean(prof_dbl[31:42])
    #print(topL, topS, np.mean(profS[31:42]))

    fig1 = plt.figure(1)

    ax = fig1.gca()

    ax.plot(prof_std,'b')
    ax.plot(prof_dbl,'r')
    #ax.plot(prof_phs,'g')
    #ax.plot(prof_rnd,'y')

    plt.show()

if __name__ == "__main__":
    main()

