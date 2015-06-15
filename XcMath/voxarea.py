# -*- coding: utf-8 -*-

import math

def circ_segment_area(R, h):
    """
    Computes half of the area of the circular segment
    
    
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
        
    if h > R:
        raise ValueError("circ_segment_area", "circle radius is smaller than height")
        
    if h == R:
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
    """
    
    xc = 0.5 * (xmin + xmax)
    yc = 0.5 * (ymin + ymax)
    
    if xc >= 0.0 and yc >= 0.0:
        return (xmin, ymin, xmax, ymax)
    
    if xc < 0.0 and yc >= 0.0:
        return (ymin, -xmax, ymax, -xmin)
        
    if xc < 0.0 and yc < 0.0:
        return (-xmax, -xmin, -xmax, -xmin)
        
    # xc > 0.0 && yc < 0.0:
    return (-ymax, xmin, -ymin, xmax)
    

def vaInner(R, xmin, ymin, xmax, ymax):
    """
    Computes intersection area
    
    Radius of the point with center of the voxel is inside the R
    """
    
    # get the points in the first quadrant
    (xmin, ymin, xmax, ymax) = rotate_voxel(xmin, ymin, xmax, ymax)
    
    rmaxmax = math.sqrt(xmax*xmax + ymax*ymax)
    if rmaxmax <= R:
        return 1.0
        
    # we know we have one corner out
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
    
def vaOuter(R, xmin, xmax, ymin, ymax):
    """
    Computes intersection area
    
    Radius of the point with center of the voxel is outside the R
    """
    
    # get the points in the first quadrant
    (xmin, ymin, xmax, ymax) = rotate_voxel(xmin, ymin, xmax, ymax)
        
    rminmin = math.sqrt(xmin*xmin + ymin*ymin)
    if rminmin <= R:
        return 1.0
        
    # we know we have one corner in
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

