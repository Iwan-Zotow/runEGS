# -*- coding: utf-8 -*-

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

    wallDescription = ""

    line = fileHandle.readline()
    if "newpath" not in line:
        raise ValueError('Invalid file format, path is supposed to start with the keyword <newpath>')

    s = line.lstrip().rstrip("\n")
    while "closepath" not in line:
        line = fileHandle.readline()
        if line.lstrip()[0:1].isalpha(): # another command
            wallDescription += s + ";"
            s = line.lstrip().rstrip("\n")
        else: # more parameters to the current line
            s += " " + line.lstrip().rstrip("\n")

    wallDescription = wallDescription + line.rstrip("\n")

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

    fiducialCurveDescription = ""

    line = fileHandle.readline()
    if "newfc" not in line:
        raise ValueError('Invalid file formath, fiducial curve is supposed to start with the keyword <newfc>')

    s = line.lstrip().rstrip("\n")
    while "closefc" not in line:
        line = fileHandle.readline()
        if line.lstrip()[0:1].isalpha(): # another command
            fiducialCurveDescription += s + ";"
            s = line.lstrip().rstrip("\n")
        else: # more parameters to the current line
            s += " " + line.lstrip().rstrip("\n")

    fiducialCurveDescription = fiducialCurveDescription + line.rstrip("\n")

    return fiducialCurveDescription
