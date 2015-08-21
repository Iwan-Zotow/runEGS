#!/usr/bin/python

import os
import fnmatch
from multiprocessing import Process

import process_cup

def process_set(set_dir, set_tag, idx_start, idx_end,  out_dir, zshift):
    """
    """
    
    pps = []
    for k in range(idx_start, idx_end+1):
    	cup_tag = "{}{:02d}".format(set_tag, k)
	p = Process(target=process_cup.process_cup, args=(set_dir, cup_tag, out_dir, zshift)) # process_cup.process_cup(set_dir, cup_tag, out_dir, zshift)
    	p.start()
	pps.append(p)
	
    for p in pps:
    	p.join()

if __name__ == "__main__":
    process_set("/home/sphinx/gcloud", "R8O3IL", 1, 9, "qqq", 140.0)
