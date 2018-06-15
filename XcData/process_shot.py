# -*- coding: utf-8 -*-

import os
import subprocess
import hashlib
import struct
import numpy as np
import logging

from XcIO     import names_helper
from XcMath   import conversion
from XcMCCore import symdata

EXT = "xz"

def check_archive_integrity(shot_name):
    """
    Given the shot archive, check compression integrity

    Parameters
    ----------

    shot_name: string
        name of the archive with compressed shot data

    returns: integer
        0 is Ok, non-zero means error
    """

    cmd = "xz -t {0}".format(shot_name)
    rc = subprocess.call(cmd, shell=True)

    return rc

def check_tar_integrity(shot_name):
    """
    Given the shot archive, check TAR integrity

    Parameters
    ----------

    shot_name: string
        name of the archive with compressed shot data

    returns: integer
        0 is Ok, non-zero means error
    """

    cmd = "tar tJf {0}".format(shot_name)
    rc = subprocess.call(cmd, shell=True)

    return rc

def unpack_archive(shot_name):
    """
    Given the shot archive, unpack it

    Parameters
    ----------

    shot_name: string
        name of the archive with compressed shot data

    returns: integer
        0 is Ok, non-zero means error
    """

    cmd = "tar xJvf {0}".format(shot_name)

    rc = subprocess.call(cmd, shell=True)

    return rc

def read_sha1(full_prefix):
    """
    Read sha1 file, return it as dictionary

    Parameters
    ----------

    full_prefix: string
        shot full prefix (e.g R8O3IL08C25_Y10Z15)

    returns: dictionary or None
        Dictionary is Ok, None if error
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

    Parameters
    ----------

    full_prefix: string
        shot full prefix (e.g R8O3IL08C25_Y10Z15)

    returns: Tuple of (bool, string, string)
        True if ok, False and file name and SHA1 if signature mismatch
    """

    shas = read_sha1(full_prefix)
    if shas == None:
        raise Exception("check_signatures", "SHA1 file is problematic")

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

    Parameters
    ----------

    full_prefix: string
        shot full prefix (e.g R8O3IL08C25_Y10Z15)

    returns: Tuple of (bool, string, string)
        True if ok, False and file name and SHA1 if signature mismatch

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

    Parameters
    ----------

    n: integer
        number of bins (boundaries are one more)

    line: string
        line contains boundaries data

    returns: array of floats
        array of parsed boundaries, in mm
    """
    split = line.split(" ")
    split = [x for x in split if x]  # remove empty lines

    boundaries = []
    for i in range(0,n+1):
        d = conversion.cm2mm( float(split[i]) )
        boundaries.append(d)

    if boundaries.count == 0:
        return None

    return boundaries

def get_full_prefix_name(shot_name):
    """
    Given shot name, get back full name

    Parameters
    ----------

    shot_name: string
        full shot file name

    returns: string
        extracted full prefix (e.g R8O3IL08C25_Y10Z15)
    """

    head,tail = os.path.split(shot_name)

    idx = tail.find(".")
    if idx == -1:
        raise ValueError("File shot not found: {0}".shot_name)

    return tail[:idx]

def get_3ddata(nx, ny, nz, line, data):
    """
    Read a line and convert it to 3D dose representation

    Parameters
    ----------

    nx: integer
        nof X points
    ny: integer
        nof Y points
    nz: integer
        nof Z points
    line: string
        which contains all 3D dose data points
    data: numpy 3D grid of floats
        3D dose data as NumPy object
    """

    split = line.split(" ")
    split = [x for x in split if x]  # remove empty lines

    k = 0
    for iz in range(0, nz):
        for iy in range(0, ny):
            for ix in range(0, nx):
                data[ix,iy,iz] = float(split[k])
                k += 1

def read_data(full_prefix):
    """
    Read shot data into data array from full prefixed dir

    Parameters
    ----------

    full_prefix: string
        directory with full prefix name, contains unpacked shot data (e.g R8O3IL08C25_Y10Z15)

    returns: symdata object
        all .3ddose data read from shot on success, None on failure
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

def writeX_d3d(fname, tddata, zshift, header):
    """
    Write X averaged dose data, assuming data is X averaged

    Parameters
    ----------

    fname: string
        file name to write

    tddata: 3d data object
        holds dose and boundaries to write

    zshift: float
        Z shift, mm

    header: 8*[int]
        array of 8 ints to write as a header

    returns: Tuple of floats
        dose bounding box (minX, maxX, minY, maxY, minZ, maxZ), in mm, or None in the case of failure
    """

    if not tddata.sym_x():
        raise Exception("Data are NOT x averaged, bailing out...\n")

    folder_name = os.path.dirname(fname)

    if folder_name != '':
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

    nx = tddata.nx()
    ny = tddata.ny()
    nz = tddata.nz()

    bx = tddata.bx()
    by = tddata.by()
    bz = tddata.bz()

    data = tddata.data()

    with open(fname, "wb") as f:
        # write 32 byte header
        f.write(struct.pack("i", np.int32(header[0]))) # 1
        f.write(struct.pack("i", np.int32(header[1]))) # 2
        f.write(struct.pack("i", np.int32(header[2]))) # 3
        f.write(struct.pack("i", np.int32(header[3]))) # 4
        f.write(struct.pack("i", np.int32(header[4]))) # 5
        f.write(struct.pack("i", np.int32(header[5]))) # 6
        f.write(struct.pack("i", np.int32(header[6]))) # 7
        f.write(struct.pack("i", np.int32(header[7]))) # 8

        # write symmetry flags
        f.write(struct.pack("i", 1)) # X sym
        f.write(struct.pack("i", 0)) # Y not sym
        f.write(struct.pack("i", 0)) # Z not sym

        # write dimensions
        nx_half = nx//2
        f.write(struct.pack("i", nx_half)) # due to symmetry
        f.write(struct.pack("i", ny))
        f.write(struct.pack("i", nz))

        # write X boundaries, symmetric
        for ix in range(nx_half, nx+1):
            xmm = np.float32( bx[ix] )
            f.write(struct.pack("f", xmm))

        # write Y boundaries, full
        for iy in range(0, ny+1):
            ymm = np.float32( by[iy] )
            f.write(struct.pack("f", ymm))

        # write Z boundaries, full
        for iz in range(0, nz+1):
            zmm = np.float32( bz[iz] ) - zshift
            f.write(struct.pack("f", zmm))

        # supposed to be reversed order
        for ix in range(nx_half, nx):
            for iy in range(0, ny):
                for iz in range(0, nz):
                    d = np.float32(data[ix,iy,iz])
                    f.write(struct.pack("f", d))

    return ( bx[0], bx[-1], by[0], by[-1], bz[0] - zshift, bz[-1] - zshift)

def writeXY_d3d(fname, tddata, zshift, header):
    """
    Write X&Y averaged dose data, assuming data is X&Y averaged

    Parameters
    ----------

    fname: string
        file name to write

    tddata: 3d data object
        holds dose and boundaries to write

    zshift: float
        Z shift, mm

    header: 8*[int]
        array of 8 ints to write as a header

    returns: Tuple of floats
        dose bounding box (minX, maxX, minY, maxY, minZ, maxZ), in mm, or None in the case of failure
    """

    if not tddata.sym_x():
        raise Exception("Data are NOT X averaged, bailing out...\n")

    if not tddata.sym_y():
        raise Exception("Data are NOT Y averaged, bailing out...\n")

    folder_name = os.path.dirname(fname)

    if folder_name != '':
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

    nx = tddata.nx()
    ny = tddata.ny()
    nz = tddata.nz()

    bx = tddata.bx()
    by = tddata.by()
    bz = tddata.bz()

    data = tddata.data()

    with open(fname, "wb") as f:
        # write 32byte header
        f.write(struct.pack("i", np.int32(header[0]))) # 1
        f.write(struct.pack("i", np.int32(header[1]))) # 2
        f.write(struct.pack("i", np.int32(header[2]))) # 3
        f.write(struct.pack("i", np.int32(header[3]))) # 4
        f.write(struct.pack("i", np.int32(header[4]))) # 5
        f.write(struct.pack("i", np.int32(header[5]))) # 6
        f.write(struct.pack("i", np.int32(header[6]))) # 7
        f.write(struct.pack("i", np.int32(header[7]))) # 8

        # write symmetry flags
        f.write(struct.pack("i", 1)) # X sym
        f.write(struct.pack("i", 1)) # Y sym
        f.write(struct.pack("i", 0)) # Z not sym

        # write dimensions
        nx_half = nx//2
        f.write(struct.pack("i", nx_half)) # due to symmetry

        ny_half = ny//2
        f.write(struct.pack("i", ny_half))

        f.write(struct.pack("i", nz))

        # write X boundaries, symmetric
        for ix in range(nx_half, nx+1):
            xmm = np.float32( bx[ix] )
            f.write(struct.pack("f", xmm))

        # write Y boundaries, symmetric
        for iy in range(ny_half, ny+1):
            ymm = np.float32( by[iy] )
            f.write(struct.pack("f", ymm))

        # write Z boundaries, full
        for iz in range(0, nz+1):
            zmm = np.float32( bz[iz] ) - zshift
            f.write(struct.pack("f", zmm))

        # supposed to be reversed order
        for ix in range(nx_half, nx):
            for iy in range(ny_half, ny):
                for iz in range(0, nz):
                    d = np.float32(data[ix,iy,iz])
                    f.write(struct.pack("f", d))

    return ( bx[0], bx[-1], by[0], by[-1], bz[0] - zshift, bz[-1] - zshift)

def full_prefix_2_d3d_name(full_prefix):
    """
    Given full prefix for a shot, make .d3difo compatible file name

    full_prefix: string
        directory with full prefix name, contains unpacked shot data (e.g R8O3IL08C25_Y10Z15)

    returns: string
        .d3difo compatible file name (e.g. R8O2IM01_Y000Z000C015)
    """

    radUnit, outerCup, innerCupSer, innerCupNum, coll = names_helper.parse_file_prefix( full_prefix )
    (shY, shZ) = names_helper.parse_shot(full_prefix)

    file_prefix = names_helper.make_cup_prefix(radUnit, outerCup, innerCupSer, innerCupNum)

    return file_prefix + "_Y{0:03d}Z{1:03d}C{2:03d}".format(int(shY), int(shZ), int(coll))

def process_shot(shot_name, out_dir, zshift, header, sym_Y = False):
    """
    Process single shot given shot full filename

    shot_name: string
        full name of the compressed shot data file

    out_dir: string
        name of the output directory

    zshift: float
        Z shift, in mm

    header: 8*[int]
        array of 8 ints to write as a header

    sym_Y: boolean
        set to true if user need symmetrized-over-Y shots

    returns: tuple of data for .d3difo file
        collimator, shot position (Y,Z) in mm, dose box bounds (minX, maxX, minY, maxY, minZ, maxZ) in mm, .d3d file name
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

    can_sym_X = tddose.could_sym_x()
    if not can_sym_X:
        raise Exception("Cannot X AVERAGE, bad X boundaries\n")

    tddose.do_sym_x()
    if not tddose.sym_x():
        raise Exception("Something went wrong on X symmetrization\n")

    can_sym_Y = False
    if sym_Y: # someone wants averaged Y
        can_sym_Y = tddose.could_sym_y() # check if we can...

    if can_sym_Y:
        # yes, we can
        tddose.do_sym_y()
        if not tddose.sym_y():
            raise Exception("Something went wrong on Y symmetrization\n")

    # writing thing out, getting back boundaries
    aname = full_prefix_2_d3d_name(full_prefix)+".d3d"
    bounds = None
    if can_sym_Y:
        bounds = writeXY_d3d(os.path.join(out_dir, aname), tddose, zshift)
    else:
        bounds = writeX_d3d(os.path.join(out_dir, aname), tddose, zshift)

    if bounds == None:
        raise Exception("No dose box bounds returned\n")

    shot   = names_helper.parse_shot(full_prefix)
    radUnit, outerCup, innerCupSer, innerCupNum, coll = names_helper.parse_file_prefix(full_prefix)

    return (coll, shot, bounds, aname)

if __name__ == "__main__":
    process_shot("/home/beamuser/Documents/EGS/R8O3IL09C25_Y0Z0.tar.xz", ".", 140.0, [1,2,3,4,5,6,7,8])
