#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import read_3ddose
import subprocess
import numpy as np
import names_helper
import logging

def dmax_shot(top, full_prefix):
    """
    Find dmax for a shot

    top: string
        top dir location

    full_prefix: string
        name of shot the compressed shot data file

    returns: tuple of data for .d3difo file
        collimator, shot position (Y,Z) in mm, dose box bounds (minX, maxX, minY, maxY, minZ, maxZ) in mm, .d3d file name
    """

    tddose = read_3ddose.read_data(top, full_prefix)

    radUnit, outerCup, innerCupSer, innerCupNum, coll = names_helper.parse_file_prefix( full_prefix )

    return (coll, shot, bounds, aname)

if __name__ == "__main__":
    dmax_shot("/home/kriol/data", "R8O1IS01C25_Y0Z0")

