# -*- coding: utf-8 -*-

import math

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
