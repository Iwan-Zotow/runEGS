#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import process_set

if __name__ == "__main__":

    # default is no symmetry over Y
    symmetrizeY = False
    if len(sys.argv) == 1:
        print("main.py <optional -y> input_dir output_dir")
        sys.exit(0)

    if len(sys.argv) > 1:
        if sys.argv[1] == "-Y" or sys.argv[1] == "-y":
            symmetrizeY = True

    pos = 1
    if symmetrizeY == True:
        pos = 2

    if len(sys.argv) < (pos+2):
        print("main.py <optional -y> input_dir output_dir")
        sys.exit(0)

    input_dir = sys.argv[pos]
    outpt_dir = sys.argv[pos+1]

    process_set.process_set(input_dir, "R8O1IS", [1,2,3,4,5,6,7,8,9],  outpt_dir, 116.0, symmetrizeY)
    process_set.process_set(input_dir, "R8O2IM", [1,2,3,4,5,6,7,8,9,10], outpt_dir, 140.0, symmetrizeY)
    process_set.process_set(input_dir, "R8O3IL", [1,2,3,4,5,6,7,8,9],  outpt_dir, 153.0, symmetrizeY)
    process_set.process_set(input_dir, "R8O0IQ", [0],  outpt_dir,  15.0, symmetrizeY)

