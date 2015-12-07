#!/usr/bin/python

from __future__ import print_function

import os
import sys

import dmax_shot

def process_list(fname):
    """
    Given file name, read list of files and process them one by one
    """

    with open(fname, 'r') as f:
        for line in f:
            head, tail = os.path.split(line)
            head, tail = os.path.split(head)

            ttt = dmax_shot.process_shot(head, tail)

            print(*ttt)

    return None

if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Need an argument - list of files")
        sys.exit(0)

    fname = sys.argv[1]

    process_list(fname)
    sys.exit(0)
