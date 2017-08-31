#%%
import sys
import os

from OCPICP import readICP, readOCP


def saveMCCurve(cname: str, zc, rc, DistanceToTop: float, TopThickness: float):
    """
    Save MC curve into fname
    """
    with open(cname, "w", encoding="utf-8") as os:
        zprev = -100000.0
        rprev = -100000.0
        for z, r in zip(zc, rc):
            if z == zprev:
                z = z - 0.001

            if r != rprev:
                os.write("{0:13.6e}  {1:13.6e}\n".format(z + DistanceToTop + TopThickness, r))

            rprev = r
            zprev = z


def cvt2MC(dir, RU, outerCup, innerCup, TopThickness = 15.0):
    """
    From .icp and .ocp produce digitized curves for MC calculations
    """
    ocp_fname = "R" + str(RU) + "O" + str(outerCup)
    icp_fname = ocp_fname + "I" + innerCup
    t = icp_fname

    ocp_fname = os.path.join(dir, ocp_fname + ".ocp")
    icp_fname = os.path.join(dir, icp_fname + ".icp")

    RUO, OCO, DistanceToTop, ziwO, riwO, zowO, rowO = readOCP(ocp_fname)
    RUI, OCI, ICI, ziwI, riwI, zowI, rowI           = readICP(icp_fname)

    if RUO != RUI:
        raise RuntimeError("RU are not the same: {0} {1}".format(RUO, RUI))

    if RUO != RU:
        raise RuntimeError("RU is not requested: {0} {1}".format(RUO, RU))

    if OCO != OCI:
        raise RuntimeError("OC are not the same: {0} {1}".format(OCO, OCI))

    if OCO != outerCup:
        raise RuntimeError("OC is not requested: {0} {1}".format(OCO, outerCup))

    #print(ICI[0], ICI[1], ICI[2], innerCup[0], innerCup[1], innerCup[2])
    if ICI != innerCup:
        raise RuntimeError("IC is not requested: {0} {1}".format(ICI, innerCup))

    saveMCCurve(t + "_KddCurveC.txt", zowO, rowO, DistanceToTop, TopThickness)
    saveMCCurve(t + "_KddCurveB.txt", ziwO, riwO, DistanceToTop, TopThickness)
    saveMCCurve(t + "_KddCurveA.txt", zowI, rowI, DistanceToTop, TopThickness)


if __name__ == "__main__":

    cvt2MC("./OICPparam/Cup.New", 8, 3, "L05")

    sys.exit(0)
