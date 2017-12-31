#!/usr/bin/env python3
"""This script compares already computed files either in directory or in the
list vs what was requested to compute (shots list). Difference is printed
on the console output
"""

import os
import sys

from XcScripts import readKdds

EXT = ".tar.xz"

def remove_shot_info(kdd):
    """
    remove shot info from kdd
    """

    idx = kdd.find("_")
    if idx < 0:
        raise RuntimeError("wrong kdd format, no shot: {0}".format(kdd))

    return kdd[0:idx]

def main(cdir, kdds, flist = None):
    """
    compare computed kdds with files in the dir,
    if flist is present, check file names in flist, otherwise check real files in directory
    """

    kdds = readKdds.readKdds(kdds_fname)

    missing = []
    for kdd in kdds:
        dname = remove_shot_info(kdd)
        fname = os.path.join(cdir, dname)
        fname = os.path.join(fname, kdd) + EXT
        # print(fname)
        if flist is None:
            if not os.path.isfile(fname):
                missing.append(kdd)
        else: # check in flist
            if fname in flist:
                pass
            else:
                missing.append(kdd)

    return missing

def read_all_computed(fname):
    """
    Read all computed shots from file and populate set
    """
    if fname is None:
        return None

    computed = set()
    with open(fname, 'r') as f:
        for line in f:
            computed.add(line.rstrip('\n'))

        if len(computed) > 0:
            return computed

    return None

if __name__ =='__main__':
    nof_args = len(sys.argv)

    if nof_args == 1 or nof_args == 2:
        print("Use: checkComputed directory list_of_KDDs <optional flist>")
        sys.exit(1)

    # nof_args >= 3
    cdir       = sys.argv[1]
    kdds_fname = sys.argv[2]

    flist = read_all_computed(sys.argv[3] if nof_args >= 4 else None)

    missing = main(cdir, kdds_fname, flist)

    if len(missing) > 0:
    	for m in missing:
            print(m)

    sys.exit(0)
