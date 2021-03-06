# -*- coding: utf-8 -*-
"""
Created on Tue May 26 15:32:05 2015 by Florin.Neacsu

Copyright Xcision LLC.
"""

from XcIOCommon import *

def ReadOCPparam(fname):
    """
    Reads the file provided as input, assuming the
    following format
    
        |Radiation unit type: int
        
        |Outer cup size: int
        
        |The signded distance between the inside bottom of the OC and the
        couch reference point in mm: float
        
        |Path of the inside wall: about 5 lines; the last line only contains
        the keyword 'closepath'
        
        |Empty line
        
        |Path of the outside wall: about 8 lines; the last line only contains
        the keyword 'closepath'
        
        |Empty line
        
        |Fiducial curve: about 10 lines; the last line only contains the
        keyword 'closefc'
    
    Parameters
    ----------
    fname: string
        A string pointing to a file on the hdd
    
    Returns
    -------
    RU: int
        The radiation unit file
    OC: int
        The outer cup size
    DistanceBottomOCToCouch: float
        The signed distance in mm from the bottom of the inner wall to the
        couch reference point
    OCInsideWallDescription: string
        A string containing the description of the inside wall. Each line is 
        separated by a ';'
    OCOutsideWallDescription: string
        A string containing the description of the outside wall. Each line is 
        separated by a ';'
    FiducialCurveDescription: string
        A string containing the description of the fiducial curve. Each line
        is separated by a ';'
    Raises
    ------
    IOError:
        If the fname is not pointing to an existing file
    ValueError:
        Whenever we try to parse to an expected format and it fails, or if
        there is an inconsitency in the values within the file
    IndexError:
        Wrong (as in unexpected) number of elements in a vector
    
    
    """
    
    
    try:
        fileHandle = open(fname, 'r')
    except IOError, e:
        e.args += ('Invalid file name',)
        raise 
    
    with fileHandle:
        try:
            line = fileHandle.readline()
            RU = int(line)
            
            line = fileHandle.readline()
            OC = int(line)
            
            line = fileHandle.readline()
            DistanceBottomOCToCouch = float(line)
            
            OCInsideWallDescription = GetWallDescription(fileHandle)
            #there is an empty line between the wall description
            #so read and discard
            line = fileHandle.readline()
            OCOutsideWallDescription = GetWallDescription(fileHandle)
            #empty line again, read and discard
            line = fileHandle.readline()
            FiducialCurveDescription = GetFiducialDescription(fileHandle)
            
            return (RU,OC,DistanceBottomOCToCouch,OCInsideWallDescription,OCOutsideWallDescription,FiducialCurveDescription)
        
        except ValueError, e:
            #raise ValueError('Invalid file format {0}\n{1}'.format(e.args, e.args))
            e.args += ('Invalid file format',)
            raise
        except IndexError, e:
            e.args += ('Invalid file format',)
            raise
            
            
            