# -*- coding: utf-8 -*-

import math

#
#    Q1   Q0
#    Q2   Q3
#
# rotation matrices
mtxQ0 = (( 1.0, 0.0), ( 0.0, 1.0))
mtxQ1 = (( 0.0, 1.0), (-1.0, 0.0))
mtxQ2 = ((-1.0, 0.0), ( 0.0,-1.0))
mtxQ3 = (( 0.0,-1.0), ( 1.0, 0.0))

def rotate(x, y, mat):
    """
    Given 2D matrix, rotate x, y pair and return rotated position
    """
    return (mat[0][0]*x + mat[0][1]*y, mat[1][0]*x + mat[1][1]*y)

def circ_segment_area(R, h):
    """
    Computes the area of the circular segment
       
    Parameters
    ----------
        
    R: float
        radius of the circle, mm
    h: float
        chord position, mm
        
    returns: float
        computed area of the circular segment divided by 2, sq.mm
    """
    
    if R <= 0.0:
        raise ValueError("circ_segment_area", "circle radius is negative or 0")
        
    if h < 0.0:
        raise ValueError("circ_segment_area", "circle radius is negative or 0")
        
    if h >= R:
        return 0.0        
        
    if h == 0.0:
        return 0.25 * math.pi * R*R
    
    theta = math.acos(h / R)
    
    return 0.5 * ( R*R*theta - h*math.sqrt((R - h)*(R + h)) )
    
def circ_segmentsector_area(R, hx, hy):
    """
    Computes half of the area of the circular segment
    
    Parameters
    ----------
        

    R: float
        radius of the circle, mm
    hx: float
        chord X position, mm        
    hy: float
        chord Y position, mm
        
    returns: float
        computed area of the circular segment sector, sq.mm
    """
    
    Sx = circ_segment_area(R, hx) 
    Sy = circ_segment_area(R, hy)
    
    return Sx + Sy + hx*hy - 0.25* math.pi * R*R
    
def rotate_voxel(xmin, ymin, xmax, ymax):
    """
    Given center position, rotate to the first quadrant
    
    Parameters
    ----------
        
    xmin: float
        low point X position, mm
    ymin: float
        low point Y position, mm
    xmax: float
        high point X position, mm
    ymax: float
        high point Y position, mm
        
    returns: floats
        properly rotated voxel in the first quadrant
    """
    
    xc = 0.5 * (xmin + xmax)
    yc = 0.5 * (ymin + ymax)
    
    if xc >= 0.0 and yc >= 0.0: # no rotation
        return (xmin, ymin, xmax, ymax)
    
    if xc < 0.0 and yc >= 0.0: # CW 90 rotation
        return (ymin, -xmax, ymax, -xmin)
        
    if xc < 0.0 and yc < 0.0: # CW 180 rotation
        return (-xmax, -ymax, -xmin, -ymin)
        
    # xc > 0.0 && yc < 0.0: # CW 270 rotation
    return (-ymax, xmin, -ymin, xmax)
    
    
def check_voxel(xmin, ymin, xmax, ymax):
    """
    Given voxel hi and low point, return true if
    voxel is good, false otherwise
    """
    return xmin < xmax and ymin < ymax

def vaInner(R, xmin, ymin, xmax, ymax):
    """
    Computes intersection area
    
    Radius of the point with center of the voxel is inside the R
    """
    
    if not check_voxel(xmin, ymin, xmax, ymax):
        raise RuntimeError("vaInner", "bad incoming voxel")
    
    #print("{0} {1} {2} {3} {4}".format(xmin, ymin, xmax, ymax, R))
    
    # get the points in the first quadrant
    (xmin, ymin, xmax, ymax) = rotate_voxel(xmin, ymin, xmax, ymax)

    if not check_voxel(xmin, ymin, xmax, ymax):
        raise RuntimeError("vaInner", "bad rotated voxel")        
    
    rmaxmax = math.sqrt(xmax*xmax + ymax*ymax)
    if rmaxmax <= R:
        return 1.0
        
    # computing other two corners
    rminmax = math.sqrt(xmin*xmin + ymax*ymax)
    rmaxmin = math.sqrt(xmax*xmax + ymin*ymin)
    
    if rminmax >= R:
        if rmaxmin >= R:
            A = circ_segmentsector_area(R, xmin, ymin)
        else: # rmaxmin < R
            A  = circ_segmentsector_area(R, xmin, ymin)
            A -= circ_segmentsector_area(R, xmax, ymin)
    else:
        if rmaxmin >= R:
            A  = circ_segmentsector_area(R, xmin, ymin)
            A -= circ_segmentsector_area(R, xmin, ymax)
        else: # rmaxmin < R
            A  = circ_segmentsector_area(R, xmin, ymin)
            A -= circ_segmentsector_area(R, xmax, ymin)
            A -= circ_segmentsector_area(R, xmin, ymax)            
        
    return A /((ymax-ymin)*(xmax-xmin))
    
def vaOuter(R, xmin, ymin, xmax, ymax):
    """
    Computes intersection area
    
    Radius of the point with center of the voxel is outside the R
    """
    
    if not check_voxel(xmin, ymin, xmax, ymax):
        raise RuntimeError("vaOuter", "bad original voxel")
        
    # get the points in the first quadrant
    (xmin, ymin, xmax, ymax) = rotate_voxel(xmin, ymin, xmax, ymax)
        
    if not check_voxel(xmin, ymin, xmax, ymax):
        raise RuntimeError("vaOuter", "bad rotated voxel")

    rminmin = math.sqrt(xmin*xmin + ymin*ymin)
    if rminmin >= R:
        return 0.0
        
    # we know we have one corner 
    rminmax = math.sqrt(xmin*xmin + ymax*ymax)
    rmaxmin = math.sqrt(xmax*xmax + ymin*ymin)
    
    if rminmax >= R:
        if rmaxmin >= R:
            A = circ_segmentsector_area(R, xmin, ymin)
        else: # rmaxmin < R
            A  = circ_segmentsector_area(R, xmin, ymin)
            A -= circ_segmentsector_area(R, xmax, ymin)
    else:
        if rmaxmin >= R:
            A  = circ_segmentsector_area(R, xmin, ymin)
            A -= circ_segmentsector_area(R, xmin, ymax)
        else: # rmaxmin < R
            A  = circ_segmentsector_area(R, xmin, ymin)
            A -= circ_segmentsector_area(R, xmax, ymin)
            A -= circ_segmentsector_area(R, xmin, ymax)            
        
    return A /((ymax-ymin)*(xmax-xmin))

