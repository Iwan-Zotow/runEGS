# -*- coding: utf-8 -*-

import os
import subprocess

DXYZ = "dosxyznrc"

def path2dosxyznrc():
    """
    Returns path to DOSXYZNRC executable
    """

    egs_path = os.environ["EGS_HOME"]
    
    if egs_path == None:
        raise RuntimeError("path2dosxyznrc", "No EGS_HOME evn.variable")
        
    return os.path.join(egs_path, DXYZ)
    
def move_results(wrk_dir, fname):
    """
    Move results from dosxyz dir to work dir
    """
    
    # just in case, take file name
    head, name = os.path.split(fname)
    
    src = os.path.join(path2dosxyznrc(), name)
    dst = fname    

    os.rename(src, dst)
    

def run_dosxyz(wrk_dir, egs_inp, pegs_inp):
    """
    run dosxyz with a given egs and pegs input files
    """
    
    process_name = DXYZ
        
    src = os.path.join(wrk_dir, egs_inp)
    lnk = os.path.join(path2dosxyznrc(), os.path.basename(egs_inp))
    
    if os.path.isfile(lnk):
        os.unlink(lnk)
        
    os.symlink(src, lnk)    

    rc = subprocess.call([process_name, "-i", os.path.basename(egs_inp), "-p", pegs_inp, "-b"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                          
    if os.path.isfile(lnk):
        os.unlink(lnk)
    
    # move the data to working folder
    name,ext = os.path.splitext(egs_inp)
    
    move_results(wrk_dir, name + ".3ddose")
    move_results(wrk_dir, name + ".errors")
    move_results(wrk_dir, name + ".egslog")
    move_results(wrk_dir, name + ".egslst")
                          
    return rc

