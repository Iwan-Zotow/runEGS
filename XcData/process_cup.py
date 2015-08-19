# -*- coding: utf-8 -*-

import os
import fnmatch
import process_shot

def write_ifo(cup_dir, out_dir, ifos, zshift):
    """
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

def process_cup(cup_dir, out_dir, zshift):
    """
    given cup dir, process all shots in cup
    """
    
    ifos = []
    k = 0
    for shot_name in os.listdir(cup_dir):
        if fnmatch.fnmatch(shot_name, "*.xz"):
        
            fname = os.path.join(cup_dir, shot_name)
            shot_data = process_shot.process_shot(fname, out_dir)
            ifos.append(shot_data)
            
            k += 1
            
            if k == 4:
                break
                
    write_ifo(cup_dir, out_dir, ifos, zshift)
            
if __name__ == "__main__":
    process_cup("/home/sphinx/gcloud/R8O3IL08C25", "qqq", -140.0)

