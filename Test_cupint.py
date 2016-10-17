# -*- coding: utf-8 -*-

import os
import sys

from XcMCCore import cup_curves
from XcMCCore import cup_linint
from XcMCCore import cup_spline

def main(json_dir: str, digi_dir: str, cup_prefix: str) -> int:
    """
    Test different cups logic
    """

    fname    = os.path.join(json_dir, cup_prefix + ".json")
    cup_crvs = cup_curves.cup_curves(fname, zshift = 0.5 + 10.28)

    fname    = os.path.join(digi_dir, cup_prefix + "_" + "KddCurveA.txt")
    cup_digi = cup_linint.cup_linint(fname)

    print("Tips drawings vs cups: {0} {1}".format(cup_crvs.zmax(), cup_digi.zmax()))

    for k in range(0, 400):
        x = 0.0 + 0.5*float(k)

        a = cup_crvs.curve(x)
        b = cup_digi.curve(x)

        print("{0}   {1}  {2}".format(x, a, b))

        if a == 0.0 and b == 0.0:
            break

    return 0

if __name__ == "__main__":

    json_dir = "/home/beamuser/Documents/EGS/runEGS/cup_geometry"
    digi_dir = "/home/beamuser/Documents/EGS/CUPS"

    cup_prefix = "R8O1IS07" # "R8O3IL07"

    rc = main(json_dir, digi_dir, cup_prefix)
    sys.exit(rc)
