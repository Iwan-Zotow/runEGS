#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import math
import fnmatch
import numpy as np

import collimator
import dmax_shot

def shots_comparator(fname):
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

    (shot_y, shot_z) = names_helper.parse_shot(full_prefix)

    # sorting over Y is preffered, Z is second order sort key
    return 1000*int(shot_y) + int(shot_z)

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
    Find dmax for all cups, give list of files

    Parameters
    ----------

    lsof: arrays of strings
        list of files with one shot per file

    returns: Tuple of (int, int, int)
        Dimensions of the 3ddose files
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
    Find min and max position of the all shots

    Parameters
    ----------

    dmax: list of (shot_x, shot_y, shot_z, dosemax)
        list of shot positions and dose

    returns: tuple of floats
        shot Y min, Y max, Z min, Z max
    """

    ymin =  10000.0
    ymax = -10000.0

    zmin =  10000.0
    zmax = -10000.0

    for (shx, shy, shz, dm) in dmax:
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

    for (shx, shy, shz, dm) in dmax:
        if math.fabs(shy - y) < 0.5:
            if math.fabs(shz - z) < 0.5:
                return dm

    return 0.0

if __name__ == "__main__":

    lsof = get_file_list("/home/kriol/data", "R8O1IS01", 25)
    dmax = dmax_all_cups(lsof)

    ymin, ymax, zmin, zmax = minmax(dmax)
    #print(ymin, ymax, zmin, zmax)

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
