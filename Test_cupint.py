#!/usr/bin/python

import sys
import os

from XcMath import linint
from XcMath import curve
from XcMath import cupint

from XcMCCore import cup_cad

def main():
    """
    Test different cups logic
    """

    wrk_dir = "C:/Users/kriol/Documents/Python/runEGS/cup_geometry"
    prefix = "R8O3IL07" # "R8O1IS07" # "R8O3IL07"

    fname = os.path.join(wrk_dir, prefix + ".json")
    cupCup = cup_cad.cup_cad(fname, zshift = 0.5 + 10.28)

    fname = os.path.join( "C:/Users/kriol/Documents/Linux/CUPS", prefix + "_" + "KddCurveA.txt")

    #liCup = cupint.cupint(cupCup, 0.5 + 10.28)
    liCCC = linint.linint(curve.curve( fname ))

    print("Tips drawings vs cups: {0} {1}".format(cupCup.zmax(), liCCC.zmax()))

    for k in range(0, 400):
        x = 0.0 + 0.5*float(k)

        #a = liCup.extrapolate(x)
        a = cupCup.curve(x)
        b = liCCC.extrapolate(x)

        print("{0}   {1}  {2}".format(x, a, b))

        if a == 0.0 and b == 0.0:
            break

    return 0

if __name__ == "__main__":

    sys.exit(main())
