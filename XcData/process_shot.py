# -*- coding: utf-8 -*-

import os
import subprocess
import symdata
import logging

EXT = "xz"

def check_archive_integrity(shot_name):
    """
    Given the shot archive, check compression integrity
    """
    
    cmd = "xz -t {0}".shot_name
    rc = subprocess.call(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    return rc

def check_tar_integrity(shot_name):
    """
    Given the shot archive, check TAR integrity
    """
    
    cmd = "tar tJvf {0}".shot_name
    rc = subprocess.call(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    return rc

def unpack_archive(shot_name)
    """
    Given the shot archive, check TAR integrity
    """
    
    cmd = "tar xJvf {0}".shot_name
    
    rc = subprocess.call(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    return rc
    
def get_dimensions(line):
    """
    Parse and extract X, Y and Z dimensions from string
    :param line: line contains x, y, z dimensions
    """
    split = line.split(" ")
    split = [x for x in split if x] # remove empty lines

    nx = int(split[0])
    ny = int(split[1])
    nz = int(split[2])

    return (nx, ny, nz)
    
def get_boundaries(n, line):
    """
    Parse and extract X, Y and Z boundaries from string
    :param n: number of bins (boundaries are one more)
    :param line: line contains boundaries data
    :returns: array of parsed boundaries
    """
    split = line.split(" ")
    split = [x for x in split if x]  # remove empty lines

    boundaries = []
    for i in range(0,n+1):
        d = float(split[i])
        boundaries.append(d)

    if boundaries.count == 0:
        return None

    return boundaries    
    
def get_full_prefix_name(shot_name):
    """
    given shot name, get back full name
    """
    
    head,tail = os.path.split(shot_name)
    
    idx = tail.find(".")
    if idx == -1
        raise ValueError("File shot not found: {0}".shot_name)

    return tail[:idx]    
    
def get_3ddata(nx, ny, nz, line, data):
    """
    Read a line and convert it to 3D dose representation
    :param nx: nof X points
    :param ny: nof Y points
    :param nz: nof Z points
    :param line" string which contains all 3D dose data points
    :returns: 3D dose data as NumPy object
    """
    split = line.split(" ")
    split = [x for x in split if x]  # remove empty lines

    k = 0
    for iz in range(0, nz):
        for iy in range(0, ny):
            for ix in range(0, nx):
                data[ix,iy,iz] = float(split[k])
                k += 1

    return None


def read_data(full_prefix):
    """
    Read shot data into data array from full prefixed dir
    """
    
    fname = os.path.join(full_prefix, full_prefix + ".3ddose")

    phd = None    
    with open(fname, 'r') as f:
        #read in the dimensions
        line = f.readline()
        (nx, ny, nz) = get_dimensions(line)

        line = f.readline()
        bx = get_boundaries(nx, line)

        line = f.readline()
        by = get_boundaries(ny, line)

        line = f.readline();
        bz = get_boundaries(nz, line)
        
        phd = symdata.symdata(bx, by, bz)
        
        data = phd.data()
        
        line = f.readline()
        get_3ddata(nx, ny, nz, line, data)        

    return phd

def process_shot(shot_name):
    """
    Process single shot given shot full filename
    """
    
    # first, check archive existance
    if not os.access(shot_name, os.R_OK):
        raise ValueError("File shot not found: {0}".shot_name)
        
    # test with decompression
    rc = check_archive_integrity(shot_name)
    if rc != 0:
        raise ValueError("Archive is bad: {0}".shot_name)
    
    rc = check_tar_integrity(shot_name)
    if rc != 0:
        raise ValueError("TAR is bad: {0}".shot_name)
              
    rc = unpack_archive(shot_name)
    if rc != 0:
        raise ValueError("Upacking failed: {0}".shot_name)
        
    tddose = read_data(shot_name)
        

