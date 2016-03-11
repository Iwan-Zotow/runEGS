import sys

from XcIO import ReadICPparam
from XcIO import ReadOCPparam

def main():
    """
    """

    RU, OC, ICType, ICSize, ZOffset, ICOrigin, ICWallEncodingType, ICInsideWallDescription, ICOutsideWallDescription = ReadICPparam.ReadICPparam("C:/Users/kriol/Documents/Python/runEGS/CADCups/InnerCups/In/R8O3IL08.icpparam")

    print(RU)
    print(OC)
    print(ICType)
    print(ICSize)
    print(ZOffset)
    print(ICOrigin)
    print(ICWallEncodingType)
    print(ICInsideWallDescription)
    print(ICOutsideWallDescription)

    print("===============================================================")

    RU,OC,DistanceBottomOCToCouch,OCInsideWallDescription,OCOutsideWallDescription,FiducialCurveDescription = ReadOCPparam.ReadOCPparam("C:/Users/kriol/Documents/Python/runEGS/CADCups/OuterCups/R8O3.ocpparam")

    print(RU)
    print(OC)
    print(DistanceBottomOCToCouch)

    print(OCInsideWallDescription)
    print(OCOutsideWallDescription)
    print(FiducialCurveDescription)


if __name__ == "__main__":
    main()

    sys.exit(0)