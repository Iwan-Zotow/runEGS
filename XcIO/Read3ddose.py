# -*- coding: utf-8 -*-
"""
Created on Thu May 14 11:18:34 2015

@author: Florin.Neacsu
"""

import numpy as np

def Read3ddose(fname):
    """
    Reads the file provided by fname as a 3ddose file with the 
    following format:
    
    |nx ny nz 
    |xBoundary
    |yBoundary
    |zBoundary
    |data
    
    where nx, ny, nz are integers providing the size in each dimension.
    xBoundary is a vector of nx+1 floats. 
    yBoundary is a vector of ny+1 floats.
    zBoundary is a vector if nz+1 floats.
    data is a vector of nx*ny*nz floats.
    
    Please note that the 3ddose file dimensions are in cm.
    
    We are using mm, so a transformation will be made while reading
    the file.
    
    Parameters
    --------
    fname: string
        A string pointing to a file on the Hdd.
    
    Returns
    -------
    nx: int
        An integer representing the size on X axis. 
    ny: int
        An integer representing the size on Y axis. 
    nz: int
        An integer representing the size on Z axis.         
    xBoundary: float[nx+1]
        A vector of nx+1 floats representing the x boundary in mm
    yBoundary: float[ny+1]
        A vector of ny+1 floats representing the y boundary in mm
    zBoundary: float[nz+1]
        A vector of nz+1 floats representing the z boundary in mm        
    dose: float[nx*ny*nz]
        A vector of nx*ny*nz floats representing the dose values
    
    Raises
    ------
    IOerror:
        In case the file doesn't exist, and IOError('Invalid file name')
        will be raised
    """
    
    try:
        fileHandle = open(fname, 'r')
    except IOError:
        #print "Could not read:", fname
        raise IOError('Invalid file name')
    
    with fileHandle:
        #read in the dimensions
            
        line = fileHandle.readline()
        (nx, ny, nz) = GetDimensions(line)
        print(nx, ny, nz)    
        line = fileHandle.readline()
        bx = GetBoundaries(nx, line)
        print(bx)    
        line = fileHandle.readline()
        by = GetBoundaries(ny, line)
        print(by)    
        line = fileHandle.readline();
        bz = GetBoundaries(nz, line)
        print(bz)    
        #create dose matrix    
        line = fileHandle.readline()
        dose3ddose = Get3ddata(nx, ny, nz, line)
        
        return (nx,ny,nz,bx,by,bz,dose3ddose)
        
        

def GetDimensions(line):
    """
    Parse and extract X, Y and Z dimensions from string
    
    Parameters
    ----------    
    line: string
        Line containing x, y, z dimensions
        
    Returns
    -------
    (nx,ny,nz): (int,int,int)
        The dimensions on x, y, and z coordinate respectively
        
    Raises
    ------
    ValueError:
        In case we try to parse a string to an int/float but the
        file is not in the expected format, this error will be raised
    """
    try:    
        split = line.split(" ")
        split = [x for x in split if x] # remove empty lines
    
        nx = int(split[0])
        ny = int(split[1])
        nz = int(split[2])
    
        return (nx, ny, nz)
    except ValueError:
            raise ValueError('Invalid file format')
    
def GetBoundaries(n, line):
    """
    Parse and extract a boundary of n+1 elements from a line
    of text
    
    Parameters
    ----------
    n: int
        Number of elements
    line: string
        line containing boundary data
    
    Returns
    -------
    
    Array of n+1 floats representing the boundary
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
    
def Get3ddata(nx, ny, nz, line):
    """
    Parses a line and converts it to 3D dose representation
    
    Parameters
    ----------    
    nx: int
        Nof X points
    ny: int
        Nof Y points
    nz: int
        Nof Z points
    line: string
        String which contains all 3D dose data points
    
    Returns
    -------
    3D dose data as NumPy object
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