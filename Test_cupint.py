#!/usr/bin/python

import sys
import os

from XcMath import linint
from XcMath import curve

from XcMCCore import cup_cad
from XcMCCore import cup_linint
from XcMCCore import cup_spline

def main():
    """
    Test different cups logic
    """

    wrk_dir = "C:/Users/kriol/Documents/Python/runEGS/cup_geometry"
    prefix = "R8O3IL07" # "R8O1IS07" # "R8O3IL07"

    fname = os.path.join(wrk_dir, prefix + ".json")
    cupCup = cup_cad.cup_cad(fname, zshift = 0.5 + 10.28)

    fname = os.path.join( "C:/Users/kriol/Documents/Linux/CUPS", prefix + "_" + "KddCurveA.txt")

    liCCC = linint.linint(curve.curve(fname))

    cl = cup_linint.cup_linint(fname)

    cs = cup_spline.cup_spline(os.path.join(wrk_dir, "R8O3IL07_SplineA.txt"))

    print("Tips drawings vs cups: {0} {1}".format(cupCup.zmax(), liCCC.zmax()))

    for k in range(0, 400):
        x = 0.0 + 0.5*float(k)

        a = cupCup.curve(x)
        b = liCCC.extrapolate(x)
        c = cl.curve(x)
        e = cs.curve(x)

        print("{0}   {1}  {2}  {3}  {4}".format(x, a, b, c, e))

        if a == 0.0 and b == 0.0:
            break

    return 0

if __name__ == "__main__":

    sys.exit(main())
