# -*- coding: utf-8 -*-
"""
Created on Sun May 10 23:57:59 2015

@author: Oleg.Krivosheev
"""

import subprocess

def run_dosxyz(egs_inp, pegs_inp):
    """
    run dosxyz with a given egs and pegs input files
    """

    process_name = "dosxyznrc"
    
    rc = subprocess.call([process_name, "-i", egs_inp, "-p", pegs_inp],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                          
    return rc  
