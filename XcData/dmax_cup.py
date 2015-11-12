#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import math
import fnmatch
import numpy as np
import matplotlib.pyplot as plt

import collimator
import dmax_shot

def shots_comparer(fname):
    """
    Shots comparator
        
    Parameters
    ----------
        
    fname: string
        shot file name with encoded shot position
        
    returns: int
        comparison key, favoring Y over Z
    """
    
    head, tail = os.path.split( fname )
    
    # remove dual extension
    full_prefix, qq = os.path.splitext(tail)
    full_prefix, qq = os.path.splitext(full_prefix)
    

    (shY, shZ) = names_helper.parse_shot(full_prefix)
    
    # sorting over Y is preffered, Z is second order sort key
    return 1000*int(shY) + shZ

def get_file_list(cups_dir, cup_tag, coll):
    """
    Find all .3ddose files
        
    Parameters
    ----------
        
    cups_dir: string
        directory with multiple cup shots
        
    cup_tag: string
        cup tag (e.g. R8O3IL04)
        
    coll: integer
        collimator diameter
        
    returns: array of string
        list of shot names, sorted Y first, Z second
    """
    
    cl = collimator.collimator(coll)
    sdir = os.path.join(cups_dir, cup_tag + str(cl))
    
    lsof = []
    
    for (dir, _, files) in os.walk(cups_dir):
        for f in files:
            if fnmatch.fnmatch(f, "*.3ddose"):
                path = os.path.join(dir, f)
                lsof.append( path )    
            
    return lsof
    
def dmax_all_cups(lsof):
    """
    """
    
    k = 0
    dmax = []
    for f in lsof:
        head, fname = os.path.split(f)
        fname, qq = os.path.splitext(fname)
        head, qq = os.path.split(head)
        
        dmax.append(dmax_shot.dmax_shot(head, fname))
        
        k += 1
        #if k > 10:
        #    break
        
    return dmax
    
def minmax(dmax):
    """
    """
    
    ymin =  10000.0
    ymax = -10000.0
    
    zmin =  10000.0
    zmax = -10000.0
    
    for (shy, shz, dm) in dmax:
        if ymin > shy:
            ymin = shy    
    
        if ymax < shy:
            ymax = shy    

        if zmin > shz:
            zmin = shz
    
        if zmax < shz:
            zmax = shz
            
    return (ymin, ymax, zmin, zmax)
    
def find_nearby_shot(y, z, dmax):
    """
    
    """
    
    for (shy, shz, dm) in dmax:
        if math.fabs(shy - y) < 0.5:
            if math.fabs(shz - z) < 0.5:
                return dm
                
    return 0.0
            
if __name__ == "__main__":
    lsof = get_file_list("/home/kriol/data", "R8O1IS01", 25)
    dmax = dmax_all_cups(lsof)
    
    ymin, ymax, zmin, zmax = minmax(dmax)
       
    print(ymin, ymax, zmin, zmax)

    step = 5.0
    ny = int( np.around((ymax - ymin)/step) ) + 1
    nz = int( np.around((zmax - zmin)/step) ) + 1
    print(ny, nz)
    
    sh_dm = np.empty((nz, ny))
    
    for iz in range(0, nz):
        z = float(iz) * step
        for iy in range(0, ny):
            y = float(iy) * step

            sh_dm[iz, iy] = find_nearby_shot(y, z, dmax)
            
    img = None    
    fig, axes = plt.subplots(1, 2, figsize=(12, 7), subplot_kw={'xticks': [], 'yticks': []})
    for ax in axes.flat:
        img = ax.imshow(sh_dm, interpolation="none")
        title = "R8O1IS01C25"
        ax.set_title(title)
        
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.25, 0.05, 0.5])
    fig.colorbar(img, cax=cbar_ax)
        
    plt.show()

