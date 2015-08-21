#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import conversion
import subprocess
import symdata
import hashlib
import struct
import numpy as np
import names_helper
import logging

EXT = "xz"

def check_archive_integrity(shot_name):
    """
    Given the shot archive, check compression integrity
    """
    
    cmd = "xz -t {0}".format(shot_name)
    rc = subprocess.call(cmd, shell=True)
    
    return rc

def check_tar_integrity(shot_name):
    """
    Given the shot archive, check TAR integrity
    """
    
    cmd = "tar tJf {0}".format(shot_name)
    rc = subprocess.call(cmd, shell=True)
    
    return rc

def unpack_archive(shot_name):
    """
    Given the shot archive, check TAR integrity
    """

    cmd = "tar xJvf {0}".format(shot_name)
    
    rc = subprocess.call(cmd, shell=True)
    
    return rc
    
def read_sha1(full_prefix):
    """
    Read sha1 file, return it as dictionary
    """
    
    fname = os.path.join(full_prefix, "sha1")
    if not os.access(fname, os.R_OK):
        return None
        
    shas = {}
    
    with open(fname, "r") as f:
        lines = f.readlines()
        
        for line in lines:
            s = line.split()
        
            idx = s[0].find(":")
            s[0] = s[0][:idx]
        
            head, name = os.path.split(s[0])
        
            shas[name] = s[1]

    return shas

def check_signatures(full_prefix):
    """
    Given unpacked direcory with full_prefix, read signatures and check against sha1
    """
    
    shas = read_sha1(full_prefix)
    
    algo = "sha1"
    if not (algo in hashlib.algorithms):
        raise Exception("check_signatures", "No SHA1 hash available")
        
    for k, v in shas.items():
        filename, extension = os.path.splitext(k)
        if extension == ".log":
            continue
        if extension == ".egsphsp1":
            continue
    
        fname = os.path.join(full_prefix, k)
        
        hasher = hashlib.sha1()
                
        with open(fname, "rb") as afile:
            buf = afile.read()
            hasher.update(buf)
                    
        s = hasher.hexdigest()
        if s != v:
            return (False, k, v)
            
    return (True, None, None)
    
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
    if idx == -1:
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

        line = f.readline()
        bz = get_boundaries(nz, line)
        
        phd = symdata.symdata(bx, by, bz)
        
        data = phd.data()
        
        line = f.readline()
        get_3ddata(nx, ny, nz, line, data)        

    return phd
    
def writeX_d3d(fname, tddata, zshift):
    """
    write X averaged dose data, assuming data is X averaged
    """
    folderName = os.path.dirname(fname)
    
    if not tddata.sym_x():
        raise 

    if folderName != '':
        if not os.path.exists(folderName):
            os.makedirs(folderName)
            
    nx = tddata.nx()
    ny = tddata.ny()
    nz = tddata.nz()

    bx = tddata.bx()
    by = tddata.by()
    bz = tddata.bz()
    
    data = tddata.data()

    with open(fname, "wb") as f:
        # write symmetry flags
        f.write(struct.pack("i", 1)) # X sym
        f.write(struct.pack("i", 0)) # Y not sym
        f.write(struct.pack("i", 0)) # Y not sym

        # write dimensions
        nx_half = nx//2
        f.write(struct.pack("i", nx_half)) # due to symmetry
        f.write(struct.pack("i", ny))
        f.write(struct.pack("i", nz))

        # write X boundaries, symmetric
        for ix in range(nx_half, nx+1):
            xmm = np.float32(conversion.cm2mm( bx[ix] ))
            f.write(struct.pack("f", xmm))

        # write Y boundaries, full
        for iy in range(0, ny+1):
            ymm = np.float32(conversion.cm2mm( by[iy] ))
            f.write(struct.pack("f", ymm))

        # write Y boundaries, full
        for iz in range(0, nz+1):
            zmm = np.float32(conversion.cm2mm( bz[iz] ) - zshift)
            f.write(struct.pack("f", zmm))

        # supposed to be reversed order
        for ix in range(nx_half, nx):
            for iy in range(0, ny):
                for iz in range(0, nz):
                    d = np.float32(data[ix,iy,iz])
                    f.write(struct.pack("f", d))
                    
    return (conversion.cm2mm(bx[0]), conversion.cm2mm(bx[-1]), conversion.cm2mm(by[0]), conversion.cm2mm(by[-1]), conversion.cm2mm(bz[0]), conversion.cm2mm(bz[-1]))
                        
                    
def full_prefix_2_d3d_name(full_prefix):
    """
    Make new style filename for d3d
    """
    
    radUnit, outerCup, innerCupSer, innerCupNum, coll = names_helper.parse_file_prefix( full_prefix )
    (shY, shZ) = names_helper.parse_shot(full_prefix)
    
    file_prefix = names_helper.make_cup_prefix(radUnit, outerCup, innerCupSer, innerCupNum)
    
    return file_prefix + "_Y{0:03d}Z{1:03d}C{2:03d}".format(int(shY), int(shZ), int(coll))

def process_shot(shot_name, out_dir, zshift):
    """
    Process single shot given shot full filename
    """
    
    # first, check archive existance
    if not os.access(shot_name, os.R_OK):
        raise ValueError("File shot not found: {0}".format(shot_name))
        
    # test with decompression
    rc = check_archive_integrity(shot_name)
    if rc != 0:
        raise ValueError("Archive is bad: {0}".format(shot_name))
    
    rc = check_tar_integrity(shot_name)
    if rc != 0:
        raise ValueError("TAR is bad: {0}".format(shot_name))
              
    rc = unpack_archive(shot_name)
    if rc != 0:
        raise ValueError("Upacking failed: {0}".format(shot_name))
        
    full_prefix      = get_full_prefix_name(shot_name)
    (rc, name, sha1) = check_signatures(full_prefix)
    if not rc:
        raise ValueError("SHA1 failed: {0}: {1}".format(name, sha1))

    tddose = read_data(full_prefix)
    
    can_avX = tddose.could_sym_x()
    if not can_avX:
        raise Exception("Cannot X AVERAGE, bad X boundaries\n")
    
    tddose.do_sym_x()

    aname = full_prefix_2_d3d_name(full_prefix)+".d3d"
    bounds = writeX_d3d(os.path.join(out_dir, aname), tddose, zshift)
    
    shot   = names_helper.parse_shot(full_prefix)
    radUnit, outerCup, innerCupSer, innerCupNum, coll = names_helper.parse_file_prefix( full_prefix )
    
    return (coll, shot, bounds, aname)

if __name__ == "__main__":
    process_shot("/home/beamuser/Documents/EGS/R8O3IL09C25_Y0Z0.tar.xz", ".", 140.0)
