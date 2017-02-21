# -*- coding: utf-8 -*-

def readKdds(fname):
    """
    Read list of KDDs from file to be calculated

    Parameters
    ------------

    fname: string
        file name of the KDDs list

    returns: list
        all KDDs from fname
    """

    listKdds=[]

    with open(fname,'r') as f:
        for line in f:
            listKdds.append(line.rstrip('\n'))

    rc = []
    for kdd in listKdds:
        q = kdd.split(" ")
        rc.append(q[0])

    return rc

