#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np

import symdata
import conversion

def get_dimensions(line):
    """
    Parse and extract X, Y and Z dimensions from string

    Parameters
    ----------

    line: string
        line contains x, y, z dimensions

    returns: Tuple of (int, int, int)
        Dimensions of the 3ddose files
    """

    split = line.split(" ")
    split = [x for x in split if x] # remove empty lines

    nx = int(split[0])
    ny = int(split[1])
    nz = int(split[2])

    return (nx, ny, nz)

def get_boundaries(n, line):
    """
    Parse and extract X, Y and Z boundaries from string

    Parameters
    ----------

    n: int
        number of bins (boundaries are one more)

    line: string
        line contains boundaries data

    returns: array of floats
        array of parsed boundaries, in mm
    """
    split = line.split(" ")
    split = [x for x in split if x]  # remove empty lines

    boundaries = []
    for i in range(0, n+1):
        d = conversion.cm2mm( float(split[i]) )
        boundaries.append(d)

    if boundaries.count == 0:
        return None

    return boundaries

def get_3ddata(nx, ny, nz, line, data):
    """
    Read a line and convert it to 3D dose representation

    Parameters
    ----------

    nx: integer
        nof X points
    ny: integer
        nof Y points
    nz: integer
        nof Z points
    line: string
        which contains all 3D dose data points
    data: numpy 3D grid of floats
        3D dose data as NumPy object
    """

    split = line.split(" ")
    split = [x for x in split if x]  # remove empty lines

    k = 0
    for iz in range(0, nz):
        for iy in range(0, ny):
            for ix in range(0, nx):
                data[ix,iy,iz] = float(split[k])
                k += 1

def read_data(top, full_prefix):
    """
    Read shot data into data array from full prefixed dir

    Parameters
    ----------

    top: string
        top directory

    full_prefix: string
        directory with full prefix name, contains unpacked shot data (e.g R8O3IL08C25_Y10Z15)

    returns: symdata object
        all .3ddose data read from shot on success, None on failure
    """

    fname = os.path.join(top, full_prefix, full_prefix + ".3ddose")

    phd = None
    with open(fname, 'r') as f:
        #read in the dimensions
        line = f.readline()
        (nx, ny, nz) = get_dimensions(line)

        line = f.readline()
        bx = get_boundaries(nx, line)

        line = f.readline()
        by = get_boundaries(ny, line)

        line = f.readline()
        bz = get_boundaries(nz, line)

        phd = symdata.symdata(bx, by, bz)

        data = phd.data()
        line = f.readline()
        get_3ddata(nx, ny, nz, line, data)

        error = phd.error()
        line = f.readline()
        get_3ddata(nx, ny, nz, line, error)

    return phd

def find_smallest_bin(b):
    """
    Take boundary non-uniform vector and find smallest bin
    assuming they are multiple of each other

    Parameters
    ----------

    b: array of floats
        boundaries, in mm

    returns: float
        minimal bin size
    """

    minb = 10000000.0
    prev = b[0]
    ll   = len(b)-1
    for k in range(0, ll):
        v     = b[k+1]
        delta = v - prev
        prev  = v

        if minb > delta:
            minb = delta

    return minb

def make_uniform_boundary(b, minb):
    """
    Having old non-uni boundary and minimal bin, construct new uniform boundary vector

    Parameters
    ----------

    b: array of floats
        non-uniform boundaries, in mm

    minb: float
        minimal bin size, mm

    returns: array of floats
        new uniform boundaries, mm
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

    Parameters
    ----------

    b: array of floats
        non-uniform boundaries, in mm

    returns: array of floats
        new uniform boundaries, mm
    """

    minb = find_smallest_bin(b) # here is minimal bin
    if minb <= 0.0:
        raise ValueError("Minb is bad: {0}".format(minb) )

    return ( make_uniform_boundary(b, minb), minb )

def expand_plane(plane, bx, by):
    """
    Take plane with boundaries bx and by and expand it

    Parameters
    ----------

    plane: 2D array of floats
        matrix of values

    bx: array of floats
        X boundaries, mm

    by: array of floats
        Y boundaries, mm

    returns: tuple of (array of floats, array of floats, 2D matrix of floats)
        new uniform X & Y boundaries, mm
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

    return (newx, newy, newplane)
