#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import fnmatch
import subprocess

import XcDefinitions
import collimator
import process_shot

def write_ifo(cup_tag, out_dir, ifos, zshift):
    """
    Writes .d3difo file for a cup
        
    Parameters
    ----------
        
    cup_tag: string
        cup tag
        
    out_dir: string
        output directory
        
    ifos: array
        list of ifo, one per shot
        
    zshift: float
        Z shift, mm
    """

    head, tail = os.path.split(cup_dir)
    fname = os.path.join(out_dir, tail + ".d3difo")
    with open(fname, "w") as f:
        for ifo in ifos:
            coll = ifo[0]
            shY, shZ = ifo[1]
            minX, maxX, minY, maxY, minZ, maxZ = ifo[2]
            aname  = ifo[3]
            shX = 0.0
            dmax = 0.0
            
            s = "+{0}  {1}  {2}  {3}  {4}   {5}  {6}  {7}  {8}  {9}  {10}  {11}\n".format(coll, shX, shY, shZ-zshift, dmax, minX, maxX, minY, maxY, minZ-zshift, maxZ-zshift, aname)
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
    
    full_prefix, = os.path.splitext(tail)
    full_prefix, = os.path.splitext(full_prefix)
    
    (shY, shZ) = names_helper.parse_shot(full_prefix)
    
    # sorting over Y is preffered, Z is second order
    return 1000*int(shY) + shZ
            
def get_sorted_file_list(cups_dir, cup_tag, coll):
    """
    """
    
    cl = collimator.collimator(coll)
    sdir = os.path.join(cups_dir, cup_tag + str(cl))
    
    lsof = []
    
    for shot_name in os.listdir(sdir):
        if fnmatch.fnmatch(shot_name, "*.xz"):
            fname = os.path.join(sdir, shot_name)
            lsof.append(fname)
            
    return sorted(lsof, key = shots_comparer)
    
def check_invariant(lsof15, lsof25):
    """
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
        tail15, = os.path.splitext(tail15)
        fullp15, = os.path.splitext(tail15)
        
        # ok, get full_prefix for C25
        head, tail25 = os.path.split( f25 )
        tail25, = os.path.splitext(tail25)
        fullp25, = os.path.splitext(tail25)

        # now compare them, they should be different only by colimator
        if len(fullp25) != len(fullp15):
            return (False, "different files: {0} {1}".format(fullp25, fullp15))
            
        s = fullp25.replace("C25", "C15")
        if s != fullp15:
            return (False, "different collimators: {0} {1}".format(fullp25, fullp15))
            
    return (True, "")
    
def merge_lsofs(lsof15, lsof25):
    """
    """
    
    l = len(lsof15) # we assume length is checked and found to be the same
    
    # lists are sorted using the same comparator, 
    combined = []
    for k in range(0, l):
        combined.append(lsof15[k])
        combined.append(lsof25[k])
    
    return combined

def process_cup(cups_dir, cup_tag, out_dir, zshift):
    """
    given cups directory and , process all shots in cup
    """
    
    lsof15 = get_sorted_file_list(cups_dir, cup_tag, XcDefinitions.C15)
    lsof25 = get_sorted_file_list(cups_dir, cup_tag, XcDefinitions.C25)
    
    check_invariant(lsof15, lsof25)
    
    allcups = merge_lsofs(lsof15, lsof25)
    
    ifos = []
    for shot_fname in allcups:
        fname = shot_fname
        shot_data = process_shot.process_shot(fname, out_dir)
        ifos.append(shot_data)
            
        idx = shot_name.find(".")
        sname = shot_name[:idx]
        subprocess.call("rm -rf ./{0}".format(sname), shell=True)

    write_ifo(cup_dir, out_dir, ifos, zshift)
            
if __name__ == "__main__":
    process_cup("/home/sphinx/gcloud", "R8O3IL08", "qqq", -140.0)
