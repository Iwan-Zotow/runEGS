# -*- coding: utf-8 -*-

from XcIO import XcIOCommon

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
            DistanceBottomOCToCouch = float(line)

            line = fileHandle.readline()
            split = line.split(" ")
            OCOrigin=[]
            OCOrigin.append(float(split[0]))
            OCOrigin.append(float(split[1]))
            OCOrigin.append(float(split[2]))

            line = fileHandle.readline()
            OCWallEncodingType = int(line)

            OCInsideWallDescription = XcIOCommon.GetWallDescription(fileHandle)

            #there is an empty line between the wall description
            #so read and discard
            line = fileHandle.readline()
            OCOutsideWallDescription = XcIOCommon.GetWallDescription(fileHandle)
            #empty line again, read and discard
            line = fileHandle.readline()
            FiducialCurveDescription = XcIOCommon.GetFiducialDescription(fileHandle)

            return (RU,OC,DistanceBottomOCToCouch,OCOrigin,OCWallEncodingType,OCInsideWallDescription,OCOutsideWallDescription,FiducialCurveDescription)

        except ValueError as e:
            #raise ValueError('Invalid file format {0}\n{1}'.format(e.args, e.args))
            e.args += ('Invalid file format',)
            raise
        except IndexError as e:
            e.args += ('Invalid file format',)
            raise

if __name__ == "__main__":
    RU,OC,DistanceBottomOCToCouch,OCOrigin,OCWallEncodingType,OCInsideWallDescription,OCOutsideWallDescription,FiducialCurveDescription = ReadOCPparam("C:/Users/kriol/Documents/Python/runEGS/CADCups/OuterCups/In/R8O3.ocpparam")

    print("Print data")
    print(RU)
    print(OC)
    print(DistanceBottomOCToCouch)

    print(OCInsideWallDescription)
    print(OCOutsideWallDescription)
    print(FiducialCurveDescription)
