# -*- coding: utf-8 -*-
"""
Created on Tue May 26 11:09:16 2015 by Florin.Neacsu

Copyright Xcision LLC.
"""

def GetWallDescription(fileHandle):
    """
    This method is used for obtaining a wall description, for Inner Cups and Outer Cups.
    It returns a string containing the wall encoding as found in the .icpparam
    or .ocpparam files, and not the point discretization.
    
    Parameters
    ----------
    fileHandle:
        A handle to the file containing the wall encoding. This also presumes
        that the file has been read until it gets to the wall description part
        
    Returns
    -------
    string
        A string containing all the lines needed to describe the wall. Each line
        is separated by ';'. The last entry should be 'closepath'
    
    Raises
    ------
    ValueError:
        If a certain parameter/keyword is expected at a given location and it is missing
        or not conform, ValueError will be invoked to indicate that the file is
        not of the expected format
    """
    
    line = fileHandle.readline()
    if "newpath" not in line:
        raise ValueError('Invalid file format, path is supposed to start with the keyword <newpath>')
    wallDescription = ''
    while "closepath" not in line:
        wallDescription = wallDescription + line + ';'        
        line = fileHandle.readline()
        
    wallDescription = wallDescription + line
    
    return wallDescription
    
def GetFiducialDescription(fileHandle):
    """
    This method is used to obtain the fiducial curve description. It returns a string
    containing multiple lines separated by ';'.
    
    Parameters
    ----------
    fileHandle:
        A handle to the file containing the fiducial curve description. This presumes
        that the file has been read until it gets to the feducial description
        
    Returns
    -------
    string:
        A string containing all the lines needed to describe the fiducial curve.
        Each line is separated by ';'. the last entry should be 'closefc'
    
    Raises
    ------
    ValueError:
        If a certain parameter/keyword is expected at a given location and it is missing
        or not conform, ValueError will be invoked to indicate that the file is
        not of the expected format
    """
    
    line = fileHandle.readline()
    if "newfc" not in line:
        raise ValueError('Invalid file formath, fiducial curve is supposed to start with the keyword <newfc>')
    fiducialCurveDescription = ''
    while "closefc" not in line:
        fiducialCurveDescription = fiducialCurveDescription + line + ';'
        line = fileHandle.readline()
    
    fiducialCurveDescription = fiducialCurveDescription + line
    
    return fiducialCurveDescription