# -*- coding: utf-8 -*-

from XcMCCore import cup_outer_cad
from XcMCCore import cup_inner_cad
from XcDefinitions import XcConstants

from XcIO import ReadOCPparam

def main():
    """
    main test function
    """

    fname_inner = "C:/Users/kriol/Documents/Python/runEGS/CADCups/InnerCups/In/R8O3IL08.icpparam"
    fname_outer = "C:/Users/kriol/Documents/Python/runEGS/CADCups/OuterCups/In/R8O3.ocpparam"

    RU, OC, DistanceBottomOCToCouch, OCOrigin, OCWallEncodingType, OCInsideWallDescription, OCOutsideWallDescription, FiducialCurveDescription = ReadOCPparam.ReadOCPparam(fname_outer)
    print(DistanceBottomOCToCouch)

    shift_z = XcConstants.COUCH_BOTTOM + DistanceBottomOCToCouch

    kA = cup_inner_cad.cup_inner_cad(fname_inner, shift_z)
    kB = cup_outer_cad.cup_outer_cad(fname_outer, shift_z, use_cup = cup_outer_cad.cup_outer_cad.USE_INNER)
    kC = cup_outer_cad.cup_outer_cad(fname_outer, shift_z, use_cup = cup_outer_cad.cup_outer_cad.USE_OUTER)

    for z in range(0, 156, 1):
        zz = float(z)
        ra = kA.curve(zz)
        rb = kB.curve(zz)
        rc = kC.curve(zz)

        print("{0}   {1}   {2}   {3}".format(z, ra, rb, rc))

if __name__ == "__main__":
    import sys

    main()

    sys.exit(0)
