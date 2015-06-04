# -*- coding: utf-8 -*-
"""
Created on Mon Jun 01 11:08:26 2015 by Florin.Neacsu

Copyright Xcision LLC.
"""

def ReadRDUparam(fname):
    """
    Reads the file provided as input, assuming the
    following format
    
        |Radiation unit type: int
        
        |Number of outer cups: int
        
        |Outer cup types: int[]
        
        |Number of inner cups associated with first outer cup: int
        
        |A list of inner cups, space separated: string
        
        | //Repeat the above two lines as many times(-1) as outer cups
        
        |Empty line
        
        |Number of collimators: int
        
        |Collimators sizes: int[]
        
        |Focus radius: float
        
        |Focus z max: float
        
        |Focus z min: float
        
        |Min velocity[mm/s] on x, y, z axis respectively, space separated: float[3]
        
        |Max velocity[mm/s] on x, y, z axis respectively, space separated: float[3]
        
        |Min acceleartion[mm/s2] on x, y, z axis respectively, space separated: float[3]
        
        |Max acceleartion[mm/s2] on x, y, z axis respectively, space separated: float[3]
        
        |Minimum collimator switch time[s]: float
    
    Parameters
    ----------
    fname: string
        A string pointing to a file on the hdd
    
    Returns
    -------
    RU: int
        Radiation unit file type
    NumberOfOC: int
        The number of outer cups
    OCType: int[]
        The sizes of the outer cups
    ListOfIC: list[list[string]]
        For each outer cup, a list of the inner cups associated with that OC
    NumberOfCollimators: int
        Total number of available collimators
    Collimators: int[]
        The sizes [mm] of the collimators
    XZFocusRadius: float
        The radius [mm] of X-Z vector of the table allowed movement
    ZFocusMax: float
        The maximum height [mm] of the allowed table movement
    ZFocusMin: float
        The minimum heigth [mm] of the allowed table movement
    XYZVelocityMin: float[3]
        A list containing the minimum velocity [mm/s] on X, Y, Z respectively
    XYZVelocityMax: float[3]
        A list containing the maximum velocity [mm/s] on X, Y, Z respectively
    XYZAccMin: float[3]
        A list containing the minimum acceleration [mm/s2] on X, Y, Z respectively
    XYZAccMax: float[3]
        A list containing the maximum acceleration [mm/s2] on X, Y, Z respectively
    CollimatorMinSwitchTime: float
        The collimator minimum switch time [s]

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
            NumberOfOC = int(line)
            
            line = fileHandle.readline()
            split = line.split(" ")
            #check if the number of OC is equal to the number of types of OC
            if (NumberOfOC!=len(split)):
                raise IndexError('Invalid file format')            
            
            OCType=[]
            for i in range(0,NumberOfOC):
                OCType.append(int(split[i]))         
            #get all the IC associated with their respective OC        
            ListOfIC=[]
            for i in range(0,NumberOfOC):
                line = fileHandle.readline()
                numberOfIC = int(line)
                
                line = fileHandle.readline()
                line = line.rstrip()# reomve carriage return, if present at the end of the string            
                split = line.split(" ")
                if(numberOfIC!=len(split)):
                    raise IndexError('Invalid file format')
                
                ListOfIC.append(split)
            
            #empty line that needs to be discarded
            fileHandle.readline()
            
            line = fileHandle.readline()
            NumberOfCollimators = int(line)
            
            line = fileHandle.readline()
            line = line.rstrip()
            split = line.split(" ")
            if (NumberOfCollimators !=len(split)):
                raise IndexError('Invalid file format')
            Collimators=[]
            for i in range(0,NumberOfCollimators):
                Collimators.append(int(split[i]))
            
            line = fileHandle.readline()
            XZFocusRadius = float(line)
            
            line = fileHandle.readline()
            ZFocusMax = float(line)
            
            line = fileHandle.readline()
            ZFocusMin = float(line)
            
            line = fileHandle.readline()
            XYZVelocityMin=ProcessLineWith3Values(line)
           
            
            line = fileHandle.readline()
            XYZVelocityMax=ProcessLineWith3Values(line)
            
            line = fileHandle.readline()
            XYZAccMin = ProcessLineWith3Values(line)
            
            line = fileHandle.readline()
            XYZAccMax = ProcessLineWith3Values(line)
            
            line = fileHandle.readline()
            CollimatorMinSwithTime = float(line)
            
            return (RU,NumberOfOC,OCType,ListOfIC,
                    NumberOfCollimators,Collimators,
                    XZFocusRadius,ZFocusMax,ZFocusMin,
                    XYZVelocityMin,XYZVelocityMax,
                    XYZAccMin,XYZAccMax,
                    CollimatorMinSwithTime)
            
        except ValueError, e:
            #raise ValueError('Invalid file format {0}\n{1}'.format(e.args, e.args))
            e.args += ('Invalid file format',)
            raise
        except IndexError, e:
            e.args += ('Invalid file format',)
            raise

def ProcessLineWith3Values(line):
    """
    """
    
    line = line.rstrip()
    split = line.split(" ")
    if (len(split)!=3):
        raise IndexError('Invalid file format')
    ReadValues=[]
    for i in range(0,3):
        ReadValues.append(float(split[i]))
    return ReadValues