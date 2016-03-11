#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

from XcIO     import names_helper
from XcMath   import linint

from XcMCCore import collimator
from XcMCCore import clinical
from XcMCCore import cup_curves

def get_clinical_X_range():
    """
    Returns clinical X range
    """
    return (-100.0, 100.0)     # in mm

def get_clinical_Y_range():
    """
    Returns clinical Y range
    """
    return (-100.0, 100.0)     # in mm

def get_clinical_Z_range():
    """
    Returns clinical Z range
    """
    return (-105.0, 100000000.0)     # in mm

def parse_input(s):
    """
    Parse input string and produce rad.unit, outer cup, inner cup, inner cup #, collimator
    """
    radUnit  = str(s[1:2])
    outerCup = str(s[3:4])
    innerCupSer = str(s[5:6])
    innerCupNum = str(s[6:8])
    coll        = int(str(s[9:11]))

    return (radUnit, outerCup, innerCupSer, innerCupNum, coll)

def make_shots_list(radUnit, outerCup, innerCupSer, innerCupNum, x_range, y_range, z_range, shstep, shmargin):
    """
    Given rad.unit, outer cup, inner cup, ranges, step size and margin,
    produce list of shots for a given conditions
    """

    cup_dir = "/home/beamuser/Documents/EGS/CUPS"

    file_prefix = clinical.make_cup_name(radUnit, outerCup, innerCupSer, innerCupNum)

    fname = os.path.join( cup_dir, file_prefix + ".json")
    liA   = cup_curves.cup_curves( fname, 0.5 + 10.28 )

    z_max = liA.zmax()

    ny_min = int(y_range[0] / shstep) - 1
    ny_max = int(y_range[1] / shstep) + 1
    #print(ny_min, ny_max)

    nz_min = int(z_range[0] / shstep) - 1
    nz_max = int(z_max / shstep) + 1
    #print(nz_min, nz_max)

    shots = []
    for iy in range(ny_min, ny_max):
        y = shstep * float(iy)
        if y < 0.0:
            continue
        for iz in range(nz_min, nz_max):
            z = shstep * float(iz)
            if z < 0.0:
                continue

            r = liA.curve(z)

            if y < r: # we're inside the inner cup
                shot = (y, z)
                shots.append(shot)

    return shots

if __name__ == "__main__":
    argc = len( sys.argv )

    if argc == 1 or argc > 2:
        print("Need cup setup as a parameter, like R8O3IL08C25")
        sys.exit(1)

    cname = sys.argv[1]

    radUnit, outerCup, innerCupSer, innerCupNum, coll = parse_input(cname)

    shots = make_shots_list(radUnit, outerCup, innerCupSer, innerCupNum, get_clinical_X_range(), get_clinical_Y_range(), get_clinical_Z_range(), 5.0, 0.0)

    cl = collimator.collimator(coll)

    file_prefix = clinical.make_cup_name(radUnit, outerCup, innerCupSer, innerCupNum)

    fname = file_prefix + str(cl) + ".shots"
    with open(fname, "wt") as f:
        for shot in shots:
            sname = names_helper.make_qualified_name(file_prefix, cl, shot)
            f.write(sname + os.linesep)

    sys.exit(0)
