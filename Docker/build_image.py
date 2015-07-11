#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os
import shutil

def copy_EGS(top):
    """
    Copy EGS from installation to docker
    """
    src = None
    try:
        src = os.environ["EGS_HOME"]
    except KeyError:
        raise RuntimeError("No EGS_HOME found, aborting")
        
    egsd = os.path.join(top, "egsnrc_mp")
    print(egsd)
    
    if os.path.isdir(egsd):
        shutil.rmtree(egsd)
        
    try:
        shutil.copytree(src, egsd)
    except Error:
        raise RuntimeError("Unable to copy EGS, aboring")
        
def copy_HEN(top):
    """
    Copy HEN_HOUSE from installation to docker
    """
    src = None
    try:
        src = os.environ["HEN_HOUSE"]
    except KeyError:
        raise RuntimeError("No HEN_HOUSE found, aborting")
        
    hend = os.path.join(top, "HEN_HOUSE")
    print(hend)
    
    if os.path.isdir(hend):
        shutil.rmtree(hend)
        
    try:
        shutil.copytree(src, hend)
    except Error:
        raise RuntimeError("Unable to copy HEN_HOUSE, aboring")

def copy_C25(top):
    """
    Copy source file
    """
    shutil.copy("/home/kriol/C25.egsphsp1", os.path.join(top, "C25.egsphsp1"))

def copy_SSH(top):
    """
    Copy SSH key file
    """
    shutil.copy("/home/kriol/known_hosts", os.path.join(top, "known_hosts"))
    
def get_repo(top):
    """
    Get python scripts from repository
    """
    rc = subprocess.call(["git", "clone", "https://github.com/Iwan-Zotow/runEGS.git"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # rc = subprocess.call(["svn", "checkout", "https://192.168.1.230/svn/XCSW/MC_simulation/MC_code/branches/oleg/PSrework/trunk", "."], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    return rc

def main():
    """
    Building Docker image
    """

    top = os.getcwd()
    
    # step 1 - make and fill runEGS
    red = os.path.join(top, "runEGS")
    print(red)
    
    if os.path.isdir(red):
        shutil.rmtree(red)

    os.mkdir(red)
    
    rc = get_repo(top)
    
    if rc != 0:
        raise RuntimeError("Unable to fetch main scripts from SVN, aborting")
        
    # step 2 - copy EGS
    copy_EGS(top)
    
    # step 3 - copy HEN_HOUSE
    copy_HEN(top)
    
    # step 4 - copy C25 phsf
    copy_C25(top)
    
    # step 5 - copy SSH key
    copy_SSH(top)
    
    # step last - build docker image
    rc = subprocess.call(["docker", "build", "-t", "ubuntu:dxyz",  "."], stderr=subprocess.PIPE)
    if rc != 0:
        raise RuntimeError("Unable to build docker image")

if __name__ == '__main__':
    main()

