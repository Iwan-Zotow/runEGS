#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import numpy as np
import matplotlib.pyplot as plt

import read_3ddose
import names_helper

def find_shot_index(b, pos):
    """
    Given boundaries and position, return B index
    """
    idx  = -1
    dist = 10000.0
    for k in range(0, len(b)):
        d = math.fabs(pos - b[k])
        if d < dist:
            dist = d
            idx  = k
            
    return idx

def dmax_shot(top, full_prefix):
    """
    Find dmax for a shot

    top: string
        top dir location

    full_prefix: string
        name of shot the compressed shot data file

    returns: float
        dose averaged around the shot
    """

    tddose = read_3ddose.read_data(top, full_prefix)
    
    can_sym_X = tddose.could_sym_x()
    if not can_sym_X:
        raise Exception("Cannot X AVERAGE, bad X boundaries\n")
    
    tddose.do_sym_x()
    if not tddose.sym_x():
        raise Exception("Something went wrong on X symmetrization\n")
    
    can_sym_Y = tddose.could_sym_y() # check if we can...
        
    if can_sym_Y:
        tddose.do_sym_y()
        if not tddose.sym_y():
            raise Exception("Something went wrong on Y symmetrization\n")    

    shot_y, shot_z = names_helper.parse_shot( full_prefix )
    
    six = find_shot_index(tddose.bx(), 0.0)
    siy = find_shot_index(tddose.by(), float(shot_y))
    siz = find_shot_index(tddose.bz(), float(shot_z))
    
    data = tddose.data()
    
    dmax = (data[six  , siy, siz] + data[six  , siy+1, siz] + data[six  , siy, siz+1] + data[six  , siy+1, siz+1] +
            data[six+1, siy, siz] + data[six+1, siy+1, siz] + data[six+1, siy, siz+1] + data[six+1, siy+1, siz+1])/8.0
            
    return shot_y, shot_z, dmax
    
def find_smallest_bin(b):
    """
    Take boundary non-uniform vector and find smallest bin
    assuming they are multiple of each other
    """
    
    minb = 10000000.0
    prev = b[0]
    for k in range(0, len(b)-1):
        v     = b[k+1]
        delta = v - prev
        prev  = v
        
        if minb > delta:
            minb = delta
            
    return minb
    
def make_uniform_boundary(b, minb):
    """
    having old non-uni boundary and minimal bin, construct new uni boundary vector
    """
    
    nof_bins = int( np.around((b[-1] - b[0])/minb) )
    
    newb = np.empty(nof_bins + 1)
    
    for k in range(0, nof_bins):
        newb[k] = b[0] + float(k)*minb
        
    newb[nof_bins] = b[-1]
    
    return newb
    
def new_boundary(b):
    """
    Take boundary non-uniform vector and produce uniform one with larger dimension
    """
    
    minb = find_smallest_bin(b) # here is minimal bin
    if minb <= 0.0:
        raise ValueError("Minb is bad: {0}".format(minb) )
    
    return ( make_uniform_boundary(b, minb), minb )
    
def expand_plane(plane, bx, by):
    """
    Take plane with boundaries bx and by and expand it
    """

    newx, dx = new_boundary(bx)
    newy, dy = new_boundary(by)
    
    newplane = np.empty((len(newx) - 1, len(newy) - 1))
    
    for ix in range(0, len(newx)-1):
        x   = bx[0] + float(ix)*dx + 0.5*dx
        iox = np.searchsorted(bx, x) - 1 # old X plane index
        for iy in range(0, len(newy)-1):
            y   = by[0] + float(iy)*dy + 0.5*dy
            ioy = np.searchsorted(by, y) - 1 # old Y plane index
            
            newplane[ix, iy] = plane[iox, ioy]
    
    return newplane
    
def plot_shot(top, full_prefix):
    """
    Read data, process it and plot it
    """

    tddose = read_3ddose.read_data(top, full_prefix)
    
    can_sym_X = tddose.could_sym_x()
    if not can_sym_X:
        raise Exception("Cannot X AVERAGE, bad X boundaries\n")
    
    tddose.do_sym_x()
    if not tddose.sym_x():
        raise Exception("Something went wrong on X symmetrization\n")
    
    can_sym_Y = tddose.could_sym_y() # check if we can...
        
    if can_sym_Y:
        tddose.do_sym_y()
        if not tddose.sym_y():
            raise Exception("Something went wrong on Y symmetrization\n")        
    
    dose  = tddose.data()
    izmax = tddose.nz()
    
    bx = tddose.bx()
    by = tddose.bx()
    
    fig, axes = plt.subplots(6, 6, figsize=(12, 6), subplot_kw={'xticks': [], 'yticks': []})
    fig.subplots_adjust(hspace=0.3, wspace=0.05)

    k = 0
    for ax in axes.flat:
        zidx = 0 + k
        if zidx >= izmax:
            zidx = izmax-1
            
        plane = dose[:,:,zidx]
        nplne = expand_plane(plane, bx, by)
            
        ax.imshow(nplne, interpolation="none")
        title = "Z idx:{0}".format(zidx)
        ax.set_title(title)
        
        k += 2
    
    return tddose


if __name__ == "__main__":
    tddose = plot_shot("/home/kriol/data/R8O1IS01C25", "R8O1IS01C25_Y35Z25")
    #tddose = plot_shot("/home/kriol/data", "R8O1IS01C25_Y0Z0")    
    
    plt.show()
    
    #t = dmax_shot("/home/kriol/data/R8O1IS01C25", "R8O1IS01C25_Y35Z25")
    #print(t)


