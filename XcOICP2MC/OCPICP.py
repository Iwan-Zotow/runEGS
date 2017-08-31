#!/usr/bin/env python3


def readICP(fname):
    """
    read ICP file and return tuple with RadUnit, OuterCup, Inner Cup and cup outer wall and inner wall
    """
    if fname is None:
        return None

    with open(fname) as f:
        # RU
        line = f.readline().rstrip('\n')
        RU = int(line)

        # Outer cup
        line = f.readline().rstrip('\n')
        OC = int(line)

        # Inner cup
        line = f.readline().rstrip('\n')
        IC = line.strip(' ')

        # nof points in the inner wall
        line = f.readline().rstrip('\n')
        niw = int(line)

        # inner wall
        riw = list()
        ziw = list()
        for k in range(niw):
            line = f.readline().rstrip('\n')
            s = line.split(' ')
            s = [x for x in s if x] # remove empty lines
            ziw.append(float(s[0]))
            riw.append(float(s[1]))

        # nof points in the outer wall
        line = f.readline().rstrip('\n')
        now = int(line)

        # outer wall
        row = list()
        zow = list()
        for k in range(now):
            line = f.readline().rstrip('\n')
            s = line.split(' ')
            s = [x for x in s if x] # remove empty lines
            zow.append(float(s[0]))
            row.append(float(s[1]))

        return (RU, OC, IC, ziw, riw, zow, row)

    return None


def readOCP(fname):
    """
    read OCP file and return tuple with RadUnit, Outer Cup, DistanceToTop and cup outer wall and inner wall
    """
    if fname is None:
        return None

    with open(fname) as f:
        # RU
        line = f.readline().rstrip('\n')
        RU = int(line)

        # Outer cup
        line = f.readline().rstrip('\n')
        OC = int(line)

        # DistanceToTop
        line = f.readline().rstrip('\n')
        dist = float(line)

        # nof points in the inner wall
        line = f.readline().rstrip('\n')
        niw = int(line)

        # inner wall
        riw = list()
        ziw = list()
        for k in range(niw):
            line = f.readline().rstrip('\n')
            s = line.split(' ')
            s = [x for x in s if x] # remove empty lines
            ziw.append(float(s[0]))
            riw.append(float(s[1]))

        # nof points in the outer wall
        line = f.readline().rstrip('\n')
        now = int(line)

        # outer wall
        row = list()
        zow = list()
        for k in range(now):
            line = f.readline().rstrip('\n')
            s = line.split(' ')
            s = [x for x in s if x] # remove empty lines
            zow.append(float(s[0]))
            row.append(float(s[1]))

        return (RU, OC, dist, ziw, riw, zow, row)

    return None
