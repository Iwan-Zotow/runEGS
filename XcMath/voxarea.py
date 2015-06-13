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

def vaInner(R, xmin, xmax, ymin, ymax):
    """
    Computes intersection area
    
    Radius of the point with center of the voxel is inside the R
    """
    
    if ymax < 0.0: # both values are negative, reflect
        ymin, ymax = math.fabs(ymax), math.fabs(ymax)
        
    if xmax < 0.0: # both values are negative, reflect
        xmin, xmax = math.fabs(xmax), math.fabs(xmax)
    
    rxy = math.sqrt(xmax*xmax + ymax*ymax)
    if rxy <= R:
        return 1.0
        
    return 1.0 
    
def vaOuter(R, xmin, xmax, ymin, ymax):
    """
    Computes intersection area
    
    Radius of the point with center of the voxel is outside the R
    """
    
    if ymax < 0.0: # both values are negative, reflect
        ymin, ymax = math.fabs(ymax), math.fabs(ymax)
        
    if xmax < 0.0: # both values are negative, reflect
        xmin, xmax = math.fabs(xmax), math.fabs(xmax)
    
    rxy = math.sqrt(xmax*xmax + ymax*ymax)

    return 1.0

