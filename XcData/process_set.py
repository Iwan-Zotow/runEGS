# -*- coding: utf-8 -*-

import os
import fnmatch

from multiprocessing import Process

from XcData import process_cup

def process_set(cups_dir, set_tag, indices, out_dir, zshift, header, sym_Y = False):
    """
    Process all shots for both collimators for a given cup tag

    Parameters
    ----------

    cups_dir: string
        location of the directories with shots for all cups for both collimators

    set_tag: string
        set tag (R8O3IL or similar)

    indices: list of integers
        list of indices

    out_dir: string
        output directory

    zshift: float
        cup Z shift relative to shot, mm

    header: 8*[int]
        array of 8 ints to write as a header

    sym_Y: boolean
        set to true if user need symmetrized-over-Y shots
    """

    if len(indices) == 0:
        return

    sy = sym_Y
    pps = []
    for k in indices:
        if len(str(k)) == 1:
            cup_tag = set_tag + "0" + str(k)
        else:
            cup_tag = set_tag + str(k)
        p = Process(target=process_cup.process_cup, args=(cups_dir, cup_tag, out_dir, zshift, header, sy)) # calls process_cup.process_cup(cups_dir, cup_tag, out_dir, zshift, sy)
        p.start()
        p.join()
        pps.append(p)

    #for p in pps:
    #	p.join()

if __name__ == "__main__":
    #process_set("/mnt/d/UTSW/R010", "R8O1IS", [1,2,3,4,5]  "/mnt/d/UTSW/Out", 116.0, [0x30313052, 2, 3, 4, 5, 6, 7, 8])
    #process_set("/mnt/d/UTSW/R010", "R8O2IM", [1,2,3,4,5,6,7,8,9,10,11], "/mnt/d/UTSW/Out", 140.0, [0x30313052, 2, 3, 4, 5, 6, 7, 8])
    process_set("/mnt/d/Data/p13", "R8O3IL", ["0", "A", "C", "D"],  "/mnt/d/Data/Out", 153.0, [0x30323052, 2, 3, 4, 5, 6, 7, 8])
    #process_set("/mnt/d/Data/p13", "R8O0IQ", [0, 1],  "/mnt/d/Data/Out",  15.0, [0x30323052, 2, 3, 4, 5, 6, 7, 8])
