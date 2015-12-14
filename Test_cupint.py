#!/usr/bin/python

import os
import sys

import linint
import curve as cc
import inner_cup
import cupint

def main():
    """
    """

    wrk_dir = "/home/kriol/Documents/EGS/runEGS/cup_geometry"
    prefix = "R8O1IS01" # "R8O1IS07" # "R8O3IL07"

    fname = os.path.join( wrk_dir, "R8O1IS00" + ".json")
    cupCup = inner_cup.inner_cup( fname )

    fname = os.path.join( "/home/kriol/Documents/EGS/CUPS", prefix + "_" + "KddCurveA.txt")
    cupCCC = cc.curve( fname )

    liCup = cupint.cupint(cupCup, 0.5 + 10.28 + 10.0)
    liCCC = linint.linint(cupCCC)

    print("Tips drawings vs cups: {0} {1}".format(liCup.zmax(), liCCC.zmax()))

    for k in range(0, 400):
        x = 0.0 + 0.5*float(k)

        a = liCup.extrapolate(x)
        b = liCCC.extrapolate(x)

        print("{0}   {1}  {2}".format(x, a, b))

        if a == 0.0 and b == 0.0:
            break

    return 0


if __name__ == "__main__":

    sys.exit(main())
