# -*- coding: utf-8 -*-

# couch parameters, in mm
COUCH_BOTTOM    = 15.0
COUCH_THICKNESS = 10.0

def MaximumInnerCupSize():
    """
    Returns the max number/id
    an inner cup could have.
    
    returns: integer
        max cup id    
    
    Currently it is 10, since M10 exists
    """
    return 10
    
def MinimumInnerCupSize():
    """
    Returns the min number/id
    an inner cup could have.
    
    returns: integer
        min cup id
    
    Currently it is 0
    """

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
        
def IsQACup(cup):
    """
    Given inner cup checks if it is QA or a clinical one
    
    Parameters
    ----------
    cup: string
        Inner cup series
    
    returns: boolean
        True if QA, False otherwise
    """
    
    if cup == "Q":
        return True
    return False

