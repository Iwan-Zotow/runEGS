#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from XcScripts import readKdds

EXT = ".tar.xz"

def remove_shot(kdd):
    """
    remove shot info from kdd
    """

    idx = kdd.find("_")
    if idx < 0:
        raise RuntimeError("wrong kdd format, no shot: {0}".format(kdd))

    return kdd[0:idx]

def main(cdir, kdds):
    """
    compare computed kdds with files in the dir
    """

    kdds = readKdds.readKdds(kdds_fname)

    missing = []
    for kdd in kdds:
        dname = remove_shot(kdd)
        fname = os.path.join(cdir, dname)
        fname = os.path.join(fname, kdd) + EXT
        # print(fname)
        if not os.path.isfile(fname):
            missing.append(kdd)

    return missing

if __name__ =='__main__':
    nof_args = len(sys.argv)

    if nof_args == 1 or nof_args == 2:
        print("Use: checkComputed directory list_of_KDDs")
        sys.exit(1)

    # nof_args >= 3
    cdir       = sys.argv[1]
    kdds_fname = sys.argv[2]

    missing = main(cdir, kdds_fname)

    if len(missing) > 0:
    	for m in missing:
            print(m)

    sys.exit(0)
