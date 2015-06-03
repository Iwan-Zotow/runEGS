# -*- coding: utf-8 -*-

import numpy as np

def mm2cm(v):
    """
    Converts value from mm to cm
        
    Parameters
    ----------
        
    v: value
        input value, mm
            
    returns:
        value in cm
    """
    
    if np.isnan(v):
        raise ValueError("mm2cm", "Not a number")
    
    return v * 0.1
    
def cm2mm(v):
    """
    Converts value from cm to cm
        
    Parameters
    ----------
        
    v: value
        input value, cm
            
    returns:
        value in mm
    """

    if np.isnan(v):
        raise ValueError("cm2mm", "Not a number")

    return v * 10.0
