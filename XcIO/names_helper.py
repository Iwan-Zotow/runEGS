# -*- coding: utf-8 -*-

EGSPHAN_EXT = ".egsphant"
EGSINP_EXT  = ".egsinp"
EGSPHSF_EXT = ".egsphsp1"

# GENERAL CONVENTION
#     outer prefix: R8O3
#       cup prefix: R8O3IL08
#      file prefix: R8O3IL08C25
#      full_prefix: R8O3IL08C25_Y0Z0

def make_cup_prefix(radUnit, outerCup, innerCupSer, innerCupNum):
    """
    Makes filename prefix given RU, OC, IC info

    Parameters
    ----------

        radUnit: string
            radiation unit

        outerCup: string
            outer cup info

        innerCupSer: string
            inner cup serial line

        innerCupNum: integer
            inner cup number

    returns: string
        clinical cup name
    """

    return "R" + str(radUnit) + "O" + str(outerCup) + "I" + str(innerCupSer) + str(innerCupNum)

def make_qualified_name(file_prefix, cl, shot):
    """
    Makes qualified name

    Parameters
    ----------

        file_prefix: string
            prefix with RU and cup info

        cl: collimator
            collimator info

        shot: (float,float) tuple
            shot position

    returns: string
        fully qualified cup name
    """
    return file_prefix + str(cl) + "_" + "Y{0}Z{1}".format(int(shot[0]),int(shot[1]))

def make_egsinput_name(full_prefix):
    """
    Makes EGS input name
    """

    return full_prefix + EGSINP_EXT

def parse_file_prefix(file_prefix):
    """
    Parse file prefix string and produce rad.unit, outer cup, inner cup, inner cup number, collimator
    """
    radUnit  = str(file_prefix[1:2])
    outerCup = str(file_prefix[3:4])
    innerCupSer = str(file_prefix[5:6])
    innerCupNum = str(file_prefix[6:8])
    coll        = int(str(file_prefix[9:11]))

    return (radUnit, outerCup, innerCupSer, innerCupNum, coll)

def parse_cup_prefix(file_prefix):
    """
    Parse cup prefix string and produce rad.unit, outer cup, inner cup, inner cup number
    """
    radUnit  = str(file_prefix[1:2])
    outerCup = str(file_prefix[3:4])
    innerCupSer = str(file_prefix[5:6])
    innerCupNum = str(file_prefix[6:8])

    return (radUnit, outerCup, innerCupSer, innerCupNum)

def outer_prefix(cup_prefix):
    """
    Take cup prefix string and produce outer cup prefix
    """

    radUnit, outerCup, innerCupSer, innerCupNum = parse_cup_prefix(cup_prefix)

    return "R" + str(radUnit) + "O" + str(outerCup)

def parse_shot(s):
    """
    Parse input string to extract shot
    """
    idx_shot = s.find("_")
    if idx_shot < 0:
        raise ValueError("No shot info in input")

    sh = s[idx_shot+1:]

    idx_Y = sh.find("Y")
    if idx_Y < 0:
        raise ValueError("No Y shot position in input")

    idx_Z = sh.find("Z")
    if idx_Z < 0:
        raise ValueError("No Z shot position in input")

    sh_Y = sh[idx_Y+1:idx_Z]
    sh_Z = sh[idx_Z+1:]

    return (float(sh_Y), float(sh_Z))

