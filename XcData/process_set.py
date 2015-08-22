#!/usr/bin/python

import os
import fnmatch
from multiprocessing import Process

import process_cup

def process_set(cups_dir, set_tag, idx_start, idx_stop,  out_dir, zshift):
    """
    Process all shots for both collimators for a given cup tag
        
    Parameters
    ----------
        
    cups_dir: string
        location of the directories with shots for all cups for both collimators
        
    set_tag: string
        set tag (R8O3IL or similar)
        
    idx_start: integer
        start cup index
        
    idx_stop: integer
        stop cup index, inclusive! So cups would be processed in the range [start, stop+1)
        
    out_dir: string
        output directory
        
    zshift: float
        cup Z shift relative to shot, mm
    """

    pps = []
    for k in range(idx_start, idx_stop + 1):
    	cup_tag = "{}{:02d}".format(set_tag, k)
	    p = Process(target=process_cup.process_cup, args=(cups_dir, cup_tag, out_dir, zshift)) # calls process_cup.process_cup(cups_dir, cup_tag, out_dir, zshift)
    	p.start()
	    pps.append(p)
	
    for p in pps:
    	p.join()

if __name__ == "__main__":
    process_set("/home/sphinx/gcloud", "R8O1IS", 1, 9,  "Out", 116.0)
    process_set("/home/sphinx/gcloud", "R8O2IM", 1, 10, "Out", 140.0)
    process_set("/home/sphinx/gcloud", "R8O3IL", 1, 9,  "Out", 153.0)

