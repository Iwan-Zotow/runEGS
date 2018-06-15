# -*- coding: utf-8 -*-

import os
import sys
import fnmatch
import subprocess

from XcDefinitions import XcConstants
from XcMCCore      import collimator
from XcData        import process_shot
from XcIO          import names_helper

def write_ifo(cup_tag, out_dir, ifos, zshift):
    """
    Writes .d3difo file for a cup

    Parameters
    ----------

    cup_tag: string
        cup tag (e.g. R8O3IL04)

    out_dir: string
        output directory

    ifos: array
        list of ifo, one per shot

    zshift: float
        Z shift, mm
    """

    fname = os.path.join(out_dir, cup_tag + ".d3difo")
    with open(fname, "w") as f:
        radUnit, outerCup, innerCupSer, innerCupNum, coll = names_helper.parse_file_prefix( cup_tag + "C00" )

        f.write(str(radUnit))
        f.write("\n")
        f.write(str(outerCup))
        f.write("\n")
        f.write( innerCupSer + innerCupNum )
        f.write("\n")
        f.write(str(len(ifos)))
        f.write("\n")

        for ifo in ifos:
            coll = ifo[0]
            shY, shZ = ifo[1]
            minX, maxX, minY, maxY, minZ, maxZ = ifo[2]
            aname  = ifo[3]
            shX = 0.0
            dmax = 0.0

            # dose box supposed to be already shifted
            s = "{0:+3d}  {1:+14.7e} {2:+14.7e} {3:+14.7e}  {4:+14.7e}  {5:+14.7e} {6:+14.7e} {7:+14.7e} {8:+14.7e} {9:+14.7e} {10:+14.7e}  {11}\n".format(coll, shX, shY, shZ-zshift, dmax, minX, maxX, minY, maxY, minZ, maxZ, aname)
            f.write(s)

def shots_comparer(fname):
    """
    Shots comparator

    Parameters
    ----------

    fname: string
        shot file name with encoded shot position

    returns: integer
        comparison key, favoring Y over Z
    """

    head, tail = os.path.split( fname )

    # remove dual extension
    full_prefix, qq = os.path.splitext(tail)
    full_prefix, qq = os.path.splitext(full_prefix)

    (shY, shZ) = names_helper.parse_shot(full_prefix)

    # sorting over Y is preffered, Z is second order sort key
    return 1000*int(shY) + shZ

def get_sorted_file_list(cups_dir, cup_tag, coll):
    """
    Writes .d3difo file for a cup

    Parameters
    ----------

    cups_dir: string
        directory with multiple cup shots

    cup_tag: string
        cup tag (e.g. R8O3IL04)

    coll: integer
        collimator diameter

    returns: array of string
        list of shot names, sorted Y first, Z second
    """

    cl = collimator.collimator(coll)
    sdir = os.path.join(cups_dir, cup_tag + str(cl))

    lsof = []

    if not os.path.isdir(sdir):
        return lsof

    for shot_name in os.listdir(sdir):
        if fnmatch.fnmatch(shot_name, "*.xz"):
            fname = os.path.join(sdir, shot_name)
            lsof.append(fname)

    return sorted(lsof, key = shots_comparer)

def check_invariant(lsof15, lsof25):
    """
    Checks if lists of shots for C15 and C25 collimators makes sense

    Parameters
    ----------

    lsof15: array of strings
        list of C15 shots

    lsof25: array of strings
        list of C25 shots

    returns: (bool, string)
        True if ok, False otherwise with string indicating what happens
    """

    if len(lsof15) != len(lsof25):
        return (False, "Different length")

    # both lists have same number of entries
    l = len(lsof15)
    for k in range(0, l):
        f15 = lsof15[k]
        f25 = lsof25[k]

        # they are both sorted, supposedly, with the same comparator

        # ok, get full_prefix for C15
        head, tail15 = os.path.split( f15 )
        tail15, qq  = os.path.splitext(tail15)
        fullp15, qq = os.path.splitext(tail15)

        # ok, get full_prefix for C25
        head, tail25 = os.path.split( f25 )
        tail25, qq  = os.path.splitext(tail25)
        fullp25, qq = os.path.splitext(tail25)

        # now compare them, they should be different only by colimator
        if len(fullp25) != len(fullp15):
            return (False, "different files: {0} {1}".format(fullp25, fullp15))

        s = fullp25.replace("C25", "C15")
        if s != fullp15:
            return (False, "different collimators: {0} {1}".format(fullp25, fullp15))

    return (True, "")

def merge_lsofs(lsof15, lsof25):
    """
    Checks if lists of shots for C15 and C25 collimators makes sense

    Parameters
    ----------

    lsof15: array of strings
        list of C15 shots

    lsof25: array of strings
        list of C25 shots

    returns: array of strings
        Merged list of shots with interleaving C15 and C25 shots
    """

    l = len(lsof15) # we assume length is checked and found to be the same for C25

    # lists are sorted using the same comparator,
    combined = []
    for k in range(0, l):
        combined.append(lsof15[k])
        combined.append(lsof25[k])

    return combined

def process_cup(cups_dir, cup_tag, out_dir, zshift, header, sym_Y = False):
    """
    Process all shots for both collimators for a given cup tag

    Parameters
    ----------

    cups_dir: string
        location of the directories with shots for both collimators

    cup_tag: string
        cup tag (e.g. R8O3IL04)

    out_dir: string
        output directory

    zshift: float
        cup Z shift relative to shot, mm

    header: 8*[int]
        array of 8 ints to write as a header

    sym_Y: boolean
        set to true if user need symmetrized-over-Y shots
    """

    lsof15 = get_sorted_file_list(cups_dir, cup_tag, XcConstants.C15)
    lsof25 = get_sorted_file_list(cups_dir, cup_tag, XcConstants.C25)

    check_invariant(lsof15, lsof25)

    allcups = merge_lsofs(lsof15, lsof25)

    sy = sym_Y

    k = 0

    ifos = []
    for shot_fname in allcups:
        fname = shot_fname
        shot_data = process_shot.process_shot(fname, out_dir, zshift, header, sy)
        ifos.append(shot_data)

        head, tail = os.path.split(shot_fname)
        sname, tail = os.path.splitext(tail)
        sname, tail = os.path.splitext(sname)

        subprocess.call("rm -rf ./{0}".format(sname), shell=True)

        k += 1

    write_ifo(cup_tag, out_dir, ifos, zshift)

if __name__ == "__main__":
    process_cup("/home/sphinx/gcloud/30Sources", "R8O2IM03",  "Out",  140.0, [1,2,3,4,5,6,7,8], True)
    process_cup("/home/sphinx/gcloud/30Sources", "R8O2IM07",  "Out",  140.0, [1,2,3,4,5,6,7,8], True)
    process_cup("/home/sphinx/gcloud/30Sources", "R8O3IL02",  "Out",  153.0, [1,2,3,4,5,6,7,8], True)
