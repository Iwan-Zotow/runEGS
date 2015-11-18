import math
import struct
import numpy as np
import argparse
import os
import sys

def cm2mm(d):
    """
    Converts cm to mm
    :param d: data in cm
    :returns: data in mm
    """
    return d*10.0

def mm2cm(d):
    """
    Converts mm to cm
    :param d: data in mm
    :returns: data in cm
    """
    return d*0.1

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

def get_3ddata(nx, ny, nz, line):
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

    data = np.empty((nx,ny,nz))

    k = 0
    for iz in range(0, nz):
        for iy in range(0, ny):
            for ix in range(0, nx):
                data[ix,iy,iz] = float(split[k])
                k += 1

    return data

def find_dmax(nx, ny, nz, data):
    """
    Finds and retuns posotion and value of maximum point in 3D data
    :param nx: X dimension
    :param ny: Y dimension
    :param nz: Z dimension
    :param data: 3D data grid
    :returns: tuple of maximum dose position and value
    """
    dmax = -999999.0
    xmax = -1
    ymax = -1
    zmax = -1
    for iz in range(0, nz):
        for iy in range(0, ny):
            for ix in range(0, nx):
                d = data[ix,iy,iz]
                if d > dmax:
                    dmax = d
                    xmax = ix
                    ymax = iy
                    zmax = iz

    return (xmax, ymax, zmax, dmax)

def could_average(n, bounds, eps):
    """
    Check if one could bounds are symmetric, and
    we could average by just summation
    :param n: number of items
    :param bounds: array of bounds, n+1 in size
    :param eps: bounds tolerance
    :returns: true if bounds are good, false otehrwise
    """
    for i in range(1, n):
        ileft_l = i - 1
        ileft_r = ileft_l + 1

        irght_l = n - i
        irght_r = irght_l + 1

        dleft = bounds[ileft_r] - bounds[ileft_l]
        drght = bounds[irght_r] - bounds[irght_l]

        delta = math.fabs(drght - dleft)
        if (delta > eps):
            return False

    # bins are equal within eps
    return True


def averageX_3ddata(nx, ny, nz, d_in, scale):
    """
    average over X plane
    :param nx: number of items in X direction
    :param ny: number of items in Y direction
    :param nz: number of items in Z direction
    :param d_in: input uncompressed 3D data
    :returns: averaged over X 3D data
    """
    data = np.empty((nx,ny,nz))

    for iz in range(0, nz):
        for iy in range(0, ny):
            for ix in range(0, nx):
                dleft = d_in[ix,iy,iz]
                drght = d_in[nx-1-ix,iy,iz]
                data[ix,iy,iz] = (dleft + drght) * scale

    return data

def averageY_3ddata(nx, ny, nz, d_in, scale):
    """
    average over X plane
    :param nx: number of items in X direction
    :param ny: number of items in Y direction
    :param nz: number of items in Z direction
    :param d_in: input uncompressed 3D data
    :returns: averaged over Y 3D data
    """
    data = np.empty((nx,ny,nz))

    for iz in range(0, nz):
        for ix in range(0, nx):
            for iy in range(0, ny):
                dleft = d_in[ix,iy,iz]
                drght = d_in[ix,ny-1-iy,iz]
                data[ix,iy,iz] = (dleft + drght) * scale

    return data

def computeX_size(nx, ny, nz):
    """
    Compute the binary .d3d file size
    :param nx: number of items in X direction
    :param ny: number of items in Y direction
    :param nz: number of items in Z direction
    :returns: size of the file where X data is averaged
    """
    sz  = 4 + 4 + 4 # symmetry flags
    sz += 4 + 4 + 4 # dims

    # boundaries
    sz += (nx // 2 + 1)*4
    sz += (ny + 1)*4
    sz += (nz + 1)*4

    # dose
    sz += (nx // 2) * ny * nz * 4

    return sz

def computeXY_size(nx, ny, nz):
    """
    Compute the binary .d3d file size
    :param nx: number of items in X direction
    :param ny: number of items in Y direction
    :param nz: number of items in Z direction
    :returns: size of the file where X&Y data is averaged
    """
    sz  = 4 + 4 + 4 # symmetry flags
    sz += 4 + 4 + 4 # dims

    # boundaries
    sz += (nx // 2 + 1)*4
    sz += (ny // 2 + 1)*4
    sz += (nz + 1)*4

    # dose
    sz += (nx // 2) * (ny // 2) * nz * 4

    return sz

def writeX_d3d(fname, nx, ny, nz, bx, by, bz, data):
    """
    write X averaged dose data, assuming data is X averaged
    """
    folderName = os.path.dirname(fname)

    if folderName != '':
        if not os.path.exists(folderName):
            os.makedirs(folderName)

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
            xmm = np.float32(cm2mm( bx[ix] ))
            f.write(struct.pack("f", xmm))

        # write Y boundaries, full
        for iy in range(0, ny+1):
            ymm = np.float32(cm2mm( by[iy] ))
            f.write(struct.pack("f", ymm))

        # write Y boundaries, full
        for iz in range(0, nz+1):
            zmm = np.float32(cm2mm( bz[iz])-163 ) #hard coded for L04
            f.write(struct.pack("f", zmm))

        # supposed to be reversed order
        for ix in range(nx_half, nx):
            for iy in range(0, ny):
                for iz in range(0, nz):
                    d = np.float32(data[ix,iy,iz])
                    f.write(struct.pack("f", d))

def writeXY_d3d(fname, nx, ny, nz, bx, by, bz, data):
    """
    write X&Y averaged dose data, assuming data is X&Y averaged
    """
    folderName = os.path.dirname(fname)

    if folderName != '':
        if not os.path.exists(folderName):
            os.makedirs(folderName)

    with open(fname, "wb") as f:
        # write symmetry flags
        f.write(struct.pack("i", 1)) # X sym
        f.write(struct.pack("i", 1)) # Y sym
        f.write(struct.pack("i", 0)) # Y not sym

        # write dimensions
        nx_half = nx//2
        f.write(struct.pack("i", nx_half)) # due to symmetry

        ny_half = ny//2
        f.write(struct.pack("i", ny_half))

        f.write(struct.pack("i", nz))

        # write X boundaries, symmetric
        for ix in range(nx_half, nx+1):
            xmm = np.float32(cm2mm( bx[ix] ))
            f.write(struct.pack("f", xmm))

        # write Y boundaries, symmetric
        for iy in range(ny_half, ny+1):
            ymm = np.float32(cm2mm( by[iy] ))
            f.write(struct.pack("f", ymm))

        # write Y boundaries, full
        for iz in range(0, nz+1):
            zmm = np.float32(cm2mm( bz[iz])-163 ) #hard coded for L04
            f.write(struct.pack("f", zmm))

        # supposed to be reversed order
        for ix in range(nx_half, nx):
            for iy in range(ny_half, ny):
                for iz in range(0, nz):
                    d = np.float32(data[ix,iy,iz])
                    f.write(struct.pack("f", d))

def main():
    """
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',help='Input file name',required=True)
    parser.add_argument('-o', '--output', help='Output file name', required=True)
    parser.add_argument('-y', '--yav', help='Average in Y', required=False)

    args = parser.parse_args()

    fname = args.input
    fnout = args.output

    should_avY = False # get it from command line
    if args.yav != None:
        should_avY = True

    # redirect stdout to a log file

    regularSTDOUT = sys.stdout
    logFilePath = "D:\\logFile3ddose_d3d.log"
    logFile = open(logFilePath,"a")
    sys.stdout = logFile

    print '----------------------------------\n'
    print ("Converting {0} ---> {1}\n\n".format(fname,fnout))

    f = open(fname, 'r')

    #read in the dimensions
    line = f.readline()
    (nx, ny, nz) = get_dimensions(line)
    print(nx, ny, nz)

    line = f.readline()
    bx = get_boundaries(nx, line)
    print(bx)

    line = f.readline()
    by = get_boundaries(ny, line)
    print(by)

    line = f.readline()
    bz = get_boundaries(nz, line)
    print(bz)

    #create dose matrix

    line = f.readline()
    dose = get_3ddata(nx, ny, nz, line)

    line = f.readline()
    errs = get_3ddata(nx, ny, nz, line)

    (xmax, ymax, zmax, dmax) = find_dmax(nx, ny, nz, dose)

    print("\n")
    print("Original 3D data")
    print(xmax, ymax, zmax, dmax)
    print(dose[xmax, ymax, zmax])
    print(errs[xmax, ymax, zmax])
    print("\n")

    can_avX = could_average(nx, bx, 0.01)
    if (can_avX == False):
        raise Exception("Cannot AVERAGE, bad X boundaries\n")

    can_avY = False
    if should_avY: # user asked for average over Y
        can_avY = could_average(ny, by, 0.01) # check if we can

    print("Averaged over Y: ")
    if can_avY:
        print("Y\n")
    else:
        print("N\n")

    doseav = averageX_3ddata(nx, ny, nz, dose, 0.5)
    errsav = averageX_3ddata(nx, ny, nz, errs, 0.5 / math.sqrt(2.0))

    if can_avY:
        doseav = averageY_3ddata(nx, ny, nz, doseav, 0.5)
        errsav = averageY_3ddata(nx, ny, nz, errsav, 0.5 / math.sqrt(2.0))

    (xmax, ymax, zmax, dmax) = find_dmax(nx, ny, nz, doseav)
    print("Averaged 3D data")
    print(xmax, ymax, zmax, dmax)
    print(doseav[xmax, ymax, zmax])
    print(errsav[xmax, ymax, zmax])
    print("\n")

    size = 0
    if not can_avY:
        size = computeX_size(nx, ny, nz)
    else:
        size = computeXY_size(nx, ny, nz)

    print("File shall be of:")
    print(size)
    print("bytes\n")

    # writing
    if not can_avY:
        writeX_d3d(fnout, nx, ny, nz, bx, by, bz, doseav)
    else:
        writeXY_d3d(fnout, nx, ny, nz, bx, by, bz, doseav)

    print("Done\n")

    sys.stdout = regularSTDOUT
    logFile.close()

