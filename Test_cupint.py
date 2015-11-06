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
    prefix = "R8O3IL08"
    
    fname = os.path.join( wrk_dir, prefix + ".json")
    cupCup = inner_cup.inner_cup( fname )
        
    fname = os.path.join( wrk_dir, prefix + "_" + "KddCurveA.txt")
    cupCCC = cc.curve( fname )

    liCup = cupint.cupint(cupCup, 11.25)
    liCCC = linint.linint(cupCCC)
    
    for k in range(0, 150):
        x = 0.0 + 1.0*float(k)
        
        a = liCup.extrapolate(x)
        b = liCCC.extrapolate(x)
        
        print("{0}   {1}  {2}".format(x, a, b))
        
        if a == 0.0 and b == 0.0:
            break
        
    return 0


if __name__ == "__main__":

    sys.exit(main())

