# -*- coding: utf-8 -*-

from __future__ import print_function

from XcDefinitions import XcConstants as XcC
from XcIO import XcIOCommon

def ReadICPparam(fname):
    """
    Reads the file provided as input, assuming the
    following format

        |Radiation unit type: int

        |Outer cup size: int

        |Inner cup size: string and int

        |Distance from the bottom of the OC to the bottom of the IC: float

        |Origin of the coordinate system: 3 floats

        |Path encoding type: int

        |Path of the inner wall: usually 5 lines; with the 5th containing
        only the keyword 'closepath'

        |Empty line

        |Path of the outer wall: usually 5 lines; with the 5th containing
        only the keyword 'closepath'


    For a path of type 1, it looks like:
        |newpath 0.000 0.000

        |arcto 38.668 14.074

        |       |59.244 49.711

        |lineto 60.669 57.793

        |closepath

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
    ICType: char
        The outer cup type isez as a char, to which this inner cup belongs
    ICSize: int
        The size of this inner cup
    ZOffset: float
        The distance between the inside bottom of IC and the inside bottom of OC
    ICOrigin: float[3]
        The IC origin in SolidWorks coordinates
    ICWallEncodingType: int
        The path type enconding
    ICInsideWallDescription: string
        A string containing the description of the inside wall. Each line is
        separated by a ';'
    ICOutsideWallDescription: string
        A string containing the description of the outside wall. Each line is
        separated by a ';'
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
    except IOError as e:
        e.args += ('Invalid file name',)
        raise

    with fileHandle:
        try:

            line = fileHandle.readline()
            RU = int(line)

            line = fileHandle.readline()
            OC = int(line)

            line = fileHandle.readline()
            ICType = line[0];
            ICSize = int(line[1:])

            #some sanity checks
            if (OC!=XcC.InnerCupSize(ICType)):
                raise ValueError('Invalid file format')
            if (ICSize>XcC.MaximumInnerCupSize()) or (ICSize<XcC.MinimumInnerCupSize()):
                raise ValueError('Invalid file format')

            line = fileHandle.readline()
            ZOffset = float(line)

            line = fileHandle.readline()
            split = line.split(" ")
            ICOrigin=[]
            ICOrigin.append(float(split[0]))
            ICOrigin.append(float(split[1]))
            ICOrigin.append(float(split[2]))

            line = fileHandle.readline()
            ICWallEncodingType = int(line)

            ICInsideWallDescription = XcIOCommon.GetWallDescription(fileHandle)
            # there is an empty line between the 2 wall descriptions
            # so reading it, and discarding
            line = fileHandle.readline()
            ICOutsideWallDescription = XcIOCommon.GetWallDescription(fileHandle)

            return (RU,OC,ICType,ICSize,ZOffset,ICOrigin,ICWallEncodingType,ICInsideWallDescription, ICOutsideWallDescription)

        except ValueError as e:
            #raise ValueError('Invalid file format {0}\n{1}'.format(e.args, e.args))
            e.args += ('Invalid file format',)
            raise
        except IndexError as e:
            e.args += ('Invalid file format',)
            raise

if __name__ == "__main__":
    RU, OC, ICType, ICSize, ZOffset, ICOrigin, ICWallEncodingType, ICInsideWallDescription, ICOutsideWallDescription = ReadICPparam("D:/Dev/InnerCups/In/R8O3IL08.icpparam") #ReadICPparam("D:/Ceres/Resource/PlanEngine/R8/Cup/R8O3IL08.icp")

    print("Print data")
    print(RU)
    print(OC)
    print(ICType)
    print(ICSize)
    print(ZOffset)
    print(ICOrigin)
    print(ICWallEncodingType)
    print(ICInsideWallDescription)
    print(ICOutsideWallDescription)
