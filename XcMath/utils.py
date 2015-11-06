# -*- coding: utf-8 -*-

def squared(v):
    """
    Returns squared value
    """
    return v*v
    
def cubed(v):
    """
    Returns cubed value
    """
    return v*v*v

def clamp(v, vmin, vmax):
    """
    Return value clamped between vmin and vmax
    """
    
    if v < vmin:
        return vmin
        
    if v > vmax:
        return vmax
        
    return v

