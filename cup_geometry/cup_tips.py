import sys
import pandas as pd

def read_and_diff(fname):
    """
    Give file name of the cup tips,
    Read and compute difference between curves and drawings
    """
    dt = pd.read_csv(fname, delim_whitespace=True)
    dt["Diff"] = dt.Curve - dt.Drawing

    return dt

def main():
    """
    """

    dtS = read_and_diff("cup_tipS.txt")
    print("=========== S ==============")
    print(dtS)
    print(" ")

    dtM = read_and_diff("cup_tipM.txt")
    print("=========== M ==============")
    print(dtM)
    print(" ")

    dtL = read_and_diff("cup_tipL.txt")
    print("=========== L ==============")
    print(dtL)
    print(" ")

if __name__ == "__main__":
    main()
    sys.exit(0)
