# -*- coding: utf-8 -*-
"""
Created on Tue May 26 09:44:22 2015 by Florin.Neacsu

Copyright Xcision LLC.
"""

def MaximumInnerCupSize():
    """
    Returns an int, representing the max number/id
    an inner cup could have.
    
    Currently it is 10, since M10 exists
    """
    return 10

    
    
def MinimumInnerCupSize():
    
    return 0


def InnerCupSize(x):
    """
    Each inner cup is defined as XYY, where X is a char representing the size
    of the outer cup, and YY is an int from 0 to 10, representing the size
    of the inner cup.
    
    Hence we need a dictionary to associate the char (a letter) to a size
    
    Parameters
    ----------
    x: char
        A letter, encoding the outer cup type
    
    Returns
    -------
    int:
        The size of the outer cup. If -1, the outer cup type was not recognized
    """
    
    return {
        'S':1,
        'M':2,
        'L':3,
        'Q':0}.get(x,-1)
        
