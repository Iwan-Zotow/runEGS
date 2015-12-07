#!/usr/bin/python

from __future__ import print_function

import os
import math
import fnmatch
import numpy as np

import collimator
import names_helper
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

    return sorted(lsof, key = shots_comparator)

def process_cup(lsof):
    """
    Find dmax, other parameters for all shots,
    given the list of files

    Parameters
    ----------

    lsof: arrays of strings
        list of files with one shot per file

    returns: list of tuples
        list of shot parameters
    """

    k = 0
    dmax_cup = []
    for f in lsof:
        head, fname = os.path.split(f)
        fname, qq = os.path.splitext(fname)
        head, qq = os.path.split(head)

        shinfo = dmax_shot.process_shot(head, fname)
        dmax_cup.append(shinfo)

        k += 1
        #if k > 10:
        #    break

    return dmax_cup

def minmax(dmax_cup):
    """
    Find min and max position of the all shots

    Parameters
    ----------

    dmax_cup: list of tuples
        each tuples has shot parameters

    returns: tuple of floats
        shot Y min, Y max, Z min, Z max
    """

    ymin =  10000.0
    ymax = -10000.0

    zmin =  10000.0
    zmax = -10000.0

    for shinfo in dmax_cup:

        shot_y = shinfo[3]
        shot_z = shinfo[4]

        if ymin > shot_y:
            ymin = shot_y

        if ymax < shot_y:
            ymax = shot_y

        if zmin > shot_z:
            zmin = shot_z

        if zmax < shot_z:
            zmax = shot_z

    return (ymin, ymax, zmin, zmax)

def find_nearby_shot(y, z, dmax):
    """
    For a given position, find and return
    best dose max

    dmax_cup: list of tuples
        each tuples has shot parameters

    returns: tuple of floats
        shot Y min, Y max, Z min, Z max
    """

    for shinfo in dmax:
        shot_y = shinfo[3]
        shot_z = shinfo[4]

        if math.fabs(shot_y - y) < 0.5:
            if math.fabs(shot_z - z) < 0.5:
                return shinfo[5]

    return 0.0

if __name__ == "__main__":
    lsof = get_file_list("/home/kriol/data", "R8O1IS01", 25)
    dmax = process_cup(lsof)

    for d in dmax:
        print(*d)
