# -*- coding: utf-8 -*-
"""
Created on Tue Jun 02 10:14:04 2015 by Florin.Neacsu

Copyright Xcision LLC.
"""

def ReadPTMparam(fname):
    """
    
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
            if (OC!=0):
                #OC should be 0 for QA cup
                raise ValueError('Invalid file format')

            line = fileHandle.readline()
            OCType = line.rstrip()
