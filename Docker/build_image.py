#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os
import shutils

def main()
    """
    Building Docker image
    """

    top = os.getcwd()
    
    # step 1 - make and fill runEGS
    red = os.path.join(top, "runEGS")
    
    shutils.rmtree(red)
    os.mkdir(red)
    
    os.chdir(red)
    
    rc = subprocess.call(["svn", "checkout", "https://192.168.1.230/svn/XCSW/MC_simulation/MC_code/branches/oleg/PSrework/trunk", "."], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if rc != 0:
        raise RuntimeError("Unable to fetch main scripts from SVN")
        os.abort()
        
    os.chdir(top)
        
    # step 2 - copy EGS
    egsd = os.path.join(top, "egsnrc_mp")
    shutils.rmtree(egsd)
    
    rc = subprocess.call(["cp", "-a", "-R", "~/egsnrc_mp", "."], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # step 3 - copy HEN_HOUSE
    hend = os.path.join(top, "HEN_HOUSE")
    shutils.rmtree(hend)
    
    rc = subprocess.call(["cp", "-a", "-R", "~/HEN_HOUSE", "."], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # step 4 - build docker image
    rc = subprocess.call(["docker", "build", "-t", "ubuntu:dxyz",  "."], stderr=subprocess.PIPE)


if __name__ == '__main__':
    main()

