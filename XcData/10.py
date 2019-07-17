# -*- coding: utf-8 -*-

import os
import fnmatch

from multiprocessing import Process

from XcData import process_cup

def process_set(cups_dir, set_tag, idx_start, idx_stop,  out_dir, zshift, header, sym_Y = False):
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

    header: 8*[int]
        array of 8 ints to write as a header

    sym_Y: boolean
        set to true if user need symmetrized-over-Y shots
    """

    sy = sym_Y
    pps = []
    for k in range(idx_start, idx_stop + 1):
        cup_tag = "{}{:02d}".format(set_tag, k)
        p = Process(target=process_cup.process_cup, args=(cups_dir, cup_tag, out_dir, zshift, header, sy)) # calls process_cup.process_cup(cups_dir, cup_tag, out_dir, zshift, sy)
        p.start()
        p.join()
        pps.append(p)

    #for p in pps:
    #	p.join()

if __name__ == "__main__":
    #process_set("/mnt/d/Data/R012", "R8O1IS", 1, 5,  "/mnt/d/Data/Out", 116.0, [0x32313052, 2, 3, 4, 5, 6, 7, 8])
    process_set("/mnt/d/Data/", "R8O2IM", 10, 10, "/mnt/d/Data/Out", 140.0, [0x33313052, 2, 3, 4, 5, 6, 7, 8])
    process_set("/mnt/d/Data/", "R8O3IL", 1, 9,  "/mnt/d/Data/Out", 153.0, [0x33313052, 2, 3, 4, 5, 6, 7, 8])
    #process_set("/mnt/d/Data", "R8O0IQ", 0, 0,  "/mnt/d/Data/Out",  15.0, [0x35313052, 2, 3, 4, 5, 6, 7, 8])
