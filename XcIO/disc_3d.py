#
# This module is about discretization of different 3d elements
# For a given element and tolerance it produces set of
# discretized (x,y) points
#

import math
import numpy as np

from XcMath import nullspace
from XcIO import disc_2d

def disc_line_segment(xs, ys, zs, xe, ye, ze, tol):
    """
    Given start (x,y,z) point and end (x,y,z) point
    return discretized array of points

    Parameter
    ---------

        xs: float
            start X

        ys: float
            start Y

        zs: float
            start Z

        xe: float
            end X

        ye: float
            end Y

        ze: float
            end Z

        tol: float
            tolerance
    """

    x = []
    y = []
    z = []

    if xs == None or ys == None or zs == None:
        return (None, None, None)
    if xe == None or ye == None or ze == None:
        return (None, None, None)

    d = math.sqrt((xe - xs)**2 + (ye - ys)**2 + (ze - zs)**2)
    K = int(d/tol) + 2

    return (np.linspace(xs, xe, num=K), np.linspace(ys, ye, num=K), np.linspace(zs, ze, num=K))

def disc_arc_segment(x1, y1, z1, x2, y2, z2, x3, y3, z3, tol):
    """
    Given current (x1,y1,z1) point and arc (x2,y2,z2 x3,y3,z3) points
    return discretized array of points

    Parameter
    ---------

        x1: float
            current X

        y1: float
            current Y

        z1: float
            current Z

        x2: float
            arc first X

        y2: float
            arc first Y

        z2: float
            arc first Z

        x3: float
            arc second X

        y3: float
            arc second Y

        z3: float
            arc second Z

        tol: float
            tolerance
    """

    if z1 == z2 and z2 == z3: # we're on the Z plane
        xs, ys = disc_2d.disc_arc_segment(x1, y1, x2, y2, x3, y3, tol)
        zs = np.empty(len(xs))
        zs.fill(z1)
        return (xs, ys, zs)

    if x1 == x2 and x2 == x3: # we're on the X plane
        ys, zs = disc_2d.disc_arc_segment(y1, z1, y2, z2, y3, z3, tol)
        xs = np.empty(len(ys))
        xs.fill(x1)
        return (xs, ys, zs)

    if y1 == y2 and y2 == y3: # we're on the X plane
        xs, zs = disc_2d.disc_arc_segment(x1, z1, x2, z2, x3, z3, tol)
        ys = np.empty(len(xs))
        ys.fill(y1)
        return (xs, ys, zs)

    A = np.array([[x1, y1, z1, 1.0], [x2, y2, z2, 1.0], [x3, y3, z3, 1.0]])

    ZA = nullspace.nullspace(A)
    Z  = nullspace.nullspace(ZA[0:2].T)

    Rx = Z[:, 0]
    Ry = Z[:, 1]
    Rz = np.cross(Rx.T, Ry.T).T

    T = [Rx, Ry, Rz].T;
    S = [[x1 x2 x3], [y1, y2, y3], [z1, z2, z3]]

    P = T * S

    xd, yd = disc_2d.disc_arc_segment( P[0,0], P[1,0], P[0,1], P[1,1], P[0,2], P[1,2], tol)

    zd = np.empty(len(Xt))
    zd.fill(1.0)

    zd *= np.mean(P[2,:])

    # transform back to 3D space
    Q = T.T * [xd, yd, zd]

    X = Q[:, 0]
    Y = Q[:, 1]
    Z = Q[:, 2]

    return (X, Y, Z)

# REQUIREMENTS
# (1) Z-axis is the rotational axis
# (2) GC[:,0]: Z-axis
#     GC[:,1]: R-axis
def disc_spiral_segment(GC, x0, y0, z0, x, y, z, tol):
    """
    Discretize spiral segment
    """

    # not implemented
    return (None, None, None)


def disc_3d(curve, tol):
    """
    Given the curve and the tolerance, produce discretized arrays for 3d
    """

    # discretized curve
    x = []
    y = []
    z = []
    # control points
    xc = []
    yc = []
    zc = []

    commands = curve.split(";")
    cur_x = None
    cur_y = None
    cur_z = None
    for command in commands:
        s = command.split(" ")

        cmd = s[0]

        if "newpath" in cmd:
            px = float(s[1])
            py = float(s[2])
            pz = float(s[3])
            x.append(px)
            y.append(py)
            z.append(pz)
            xc.appned(px)
            yc.appned(py)
            zc.appned(pz)
            cur_x = px
            cur_y = py
            cur_z = pz

        elif "lineto" in cmd:
            px = float(s[1])
            py = float(s[2])
            pz = float(s[3])

            xs, ys, zs = disc_line_segment(cur_x, cur_y, cur_z, px, py, pz, tol)
            x.extend(xs)
            y.extend(ys)
            z.extend(zs)
            xc.append(px)
            yc.append(py)
            zc.append(pz)
            cur_x = px
            cur_y = py
            cur_z = pz

        elif "arcto" in cmd:
            x2 = float(s[1])
            y2 = float(s[2])
            z2 = float(s[3])
            x3 = float(s[4])
            y3 = float(s[5])
            z3 = float(s[6])

            xs, ys, zs = disc_arc_segment(cur_x, cur_y, cur_z, x2, y2, z2, x3, y3, z3, tol)
            x.extend(xs)
            y.extend(ys)
            z.extend(zs)

            xc.extend([x2, x3])
            yc.extend([y2, y3])
            zc.extend([z2, z3])

            cur_x = x3
            cur_y = y3
            cur_z = z3

        elif "closepath" in cmd:
            break

        else:
            raise RuntimeError("disc_3d::unknown command {0}".format(cmd))

    return (np.asarray(x), np.asarray(y, np.asarray(z), np.asarray(xc), np.asarray(yc), np.asarray(zc))

def disc_fiducial(curve, tol):
    """
    Given the curve and the tolerance, produce discretized arrays
    """

    # discretized curve
    x = []
    y = []
    z = []
    # control points
    xc = []
    yc = []
    zc = []

    commands = curve.split(";")
    cur_x = None
    cur_y = None
    cur_z = None

    for command in commands:
        s = command.split(" ")
        s = [q for q in s if q] # remove empty strings

        cmd = s[0]

        if "newfcsegment" in cmd:
            px = float(s[1])
            py = float(s[2])
            pz = float(s[3])
            x.append(px)
            y.append(py)
            z.append(pz)
            xc.appned(px)
            yc.appned(py)
            zc.appned(pz)
            cur_x = px
            cur_y = py
            cur_z = pz

        elif "lineto" in cmd:
            px = float(s[1])
            py = float(s[2])
            pz = float(s[3])

            xs, ys, zs = disc_line_segment(cur_x, cur_y, cur_z, px, py, pz, tol)
            x.extend(xs)
            y.extend(ys)
            z.extend(zs)
            xc.append(px)
            yc.append(py)
            zc.append(pz)
            cur_x = px
            cur_y = py
            cur_z = pz

        elif "arcto" in cmd:
            x2 = float(s[1])
            y2 = float(s[2])
            z2 = float(s[3])
            x3 = float(s[4])
            y3 = float(s[5])
            z3 = float(s[6])

            xs, ys, zs = disc_arc_segment(cur_x, cur_y, cur_z, x2, y2, z2, x3, y3, z3, tol)
            x.extend(xs)
            y.extend(ys)
            z.extend(zs)

            xc.extend([x2, x3])
            yc.extend([y2, y3])
            zc.extend([z2, z3])

            cur_x = x3
            cur_y = y3
            cur_z = z3

        elif "spiralto" in cmd:
            n = float(s[1])

            for k range(0, n):
                pass # read all data
            xs, ys, zs = disc_spiral_segment(None, tol)
            x.extend(xs)
            y.extend(ys)
            z.extend(zs)

            xc.extend(None)
            yc.extend(None)
            zc.extend(None)

            cur_x = x3
            cur_y = y3
            cur_z = z3

        elif "closefcsegment" in cmd:
            break

        else:
            raise RuntimeError("disc_3d::unknown command {0}".format(cmd))

    return (np.asarray(x), np.asarray(y, np.asarray(z), np.asarray(xc), np.asarray(yc), np.asarray(zc))
