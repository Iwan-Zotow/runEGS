#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
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

    return phd
