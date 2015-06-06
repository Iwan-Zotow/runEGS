# -*- coding: utf-8 -*-

import os
import subprocess

DXYZ = "dosxyznrc"

def path2dosxyznrc():
    """
    """
    egs_path = os.environ["EGS_HOME"]
    
    if egs_path == None:
        raise RuntimeError("path2dosxyznrc", "No EGS_HOME evn.variable")
        
    return os.path.join(egs_path, DXYZ)
    
def move_results(fname):
    src = os.path.join(path2dosxyznrc(), fname)
    dst = os.path.join(os.getcwd(), fname)
    
    os.rename(src, dst)
    

def run_dosxyz(egs_inp, pegs_inp):
    """
    run dosxyz with a given egs and pegs input files
    """
    
    process_name = DXYZ
    
    src = os.path.join(os.getcwd(), egs_inp)
    lnk = os.path.join(path2dosxyznrc(), egs_inp)
    
    os.symlink(src, lnk)

    rc = subprocess.call([process_name, "-i", egs_inp, "-p", pegs_inp, "-b"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                          
    os.unlink(lnk)
    
    name,ext = os.path.splitext(egs_inp)
    
    move_results(name + ".3ddose")
    move_results(name + ".errors")
    move_results(name + ".egslog")
    move_results(name + ".egslst")
                          
    return rc  
