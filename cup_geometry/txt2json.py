#!/usr/bin/python

import sys
import math
import json

N = -100
S = 0
M = 1
L = 2

# those parameters are one per cup
H0 = {0 : 2.53, 1 : 2.53, 2 : 2.53}
D5 = {0 : 93.71, 1 : 121.71, 2 : 153.71}

IS = {0 : "S", 1 : "M", 2 : "L"}

def is_a_good_cup(cup):
    """
    Returns True if cup is of the good ones, False otherwise
    """

    if cup == S:
        return True

    if cup == M:
        return True

    if cup == L:
        return True

    return False

def read_single_cup(f):
    """
    Given the file f, read whole cup info -
    cup number and then 6 digits for the shape

    Returns tuple of the all data
    """

    try:
        pos    = f.tell()
        cupnum = int(f.readline())
    except:
        # ok, this is not a cup, roll back
        f.seek(pos)
        return None

    R1 = math.fabs( float(f.readline()) )
    D1 = math.fabs( float(f.readline()) )
    H1 = math.fabs( float(f.readline()) )

    R2 = math.fabs( float(f.readline()) )
    D2 = math.fabs( float(f.readline()) )
    H2 = math.fabs( float(f.readline()) )

    return (cupnum, R1, D1, H1, R2, D2, H2)

def read_cup_series(f, cup):
    """
    Given file f, read whole cup series
    """

    while True:
        rh = read_single_cup(f) # get RH info and
        if rh == None:
            break

        write_cup(rh, cup)

def make_fname(cup, cupnum):
    """
    Make conformal cup JSON file name
    """

    assert( is_a_good_cup(cup) )

    fname  = "R8"
    fname += "O" + str(cup) + "I" + IS[cup]

    if cupnum < 10:
        fname += " "

    fname += str(cupnum)

    return fname

def write_cup(rh, cup):
    """
    Given RH data read from .txt file, write conforming JSON file
    """

    assert( is_a_good_cup(cup) )

    cupnum, R1, D1, H1, R2, D2, H2 = rh

    data = dict()

    data["cup_series"] = IS[cup]
    data["cup_number"] = cup
    data["units"]      = "mm"

    data["H0"] = H0[cup]

    data["R1"] = R1
    data["H1"] = H1
    data["D1"] = D1

    data["R2"] = R2
    data["H2"] = H2
    data["D2"] = D2

    data["D5"] = D5[cup]

    fname = make_fname(cup, cupnum) + ".json"

    with open(fname, "w") as outfile:
        json.dump(data, outfile)

def read_all_cups(fname):
    """
    Read text file with all cups
    """

    with open(fname, 'r') as f:

        while True:
            line = f.readline()

            cup = N
            if "LLL" in line:
                cup = L
            elif "MMM" in line:
                cup = M
            elif "SSS" in line:
                cup = S

            if cup == N:
                break

            read_cup_series(f, cup)

    return 0

if __name__ == "__main__":
    #if len(sys.argv) == 1:
    #    sys.exit(0)

    read_all_cups("allcupsLMS.txt")