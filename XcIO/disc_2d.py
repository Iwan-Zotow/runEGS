#
# This module is about discretization of different 2d elements
# For a given element and tolerance it produces set of
# discretized (x,y) points
#

import math
import numpy as np

from XcMath import nullspace
from XcMath import ispolycw

def disc_line_segment(sx, sy, ex, ey, tol):
    """
    Given start (x,y) point and end (x,y) point
    return discretized array of points

    Parameter
    ---------

        sx: float
            start X

        sy: float
            start Y

        ex: float
            end X

        ey: float
            end Y

        tol: float
            tolerance
    """

    x = []
    y = []

    if sx == None or sy == None:
        return (None,None)
    if ex == None or ey == None:
        return (None, None)

    d = math.sqrt((xe-xs)**2 + (ye-ys)**2)
    K = int(d/tol) + 2

    return (np.linspace(xs, xe, num=K), np.linspace(ys, ye, num=K))

def disc_arc_segment(x1, y1, x2, y2, x3, y3, tol):
    """
    Given current (x1,y1) point and arc (x2,y2, x3, y3) points
    return discretized array of points

    Parameter
    ---------

        x1: float
            current X

        y1: float
            current Y

        x2: float
            arc first X

        y2: float
            arc first Y

        x3: float
            arc second X

        y3: float
            arc second Y

        tol: float
            tolerance
    """

    A = np.array([[x1*x1+y1*y1, x1, y1, 1.0], [x2*x2+y2*y2, x2, y2, 1.0], [x3*x3+y3*y3, x3, y3, 1.0]])
    Z = nullspace.nullspace(A)

    # (x*x+y*y) + bx + cy + d = 0;
    if Z[0,0] == 0.0:
        return (None, None)

    b = Z[1,0] / Z[0,0]
    c = Z[2,0] / Z[0,0]
    d = Z[3,0] / Z[0,0]

    # center of the supporting circle (x-xo)^2 + (y-yo)^2 = r^2
    # determine the polar form
    #  x = xo + r cos(theta)
    #  y = yo + r sin(theta)

    xo = - 0.5 * b
    yo = - 0.5 * c
    r  = math.sqrt( xo*xo + yo*yo - d)

    # determine clockwiseness
    clockwise = ispolycw.ispolycw([x1, x2, x3], [y1, y2, y3])

    atan2(imag(z),real(z))
    thetas = math.atan2( y1 - yo, x1 - xo )
    thetae = math.atan2( y3 - yo, x3 - xo )

    if clockwise:
        if thetae > thetas:
            thetas += 2.0 * math.pi;
    else:
        if thetae < thetas:
            thetae += 2.0 * math.pi;

    K = int( r * math.abs(thetas - thetae) / tol ) + 2
    q = np.linspace(thetas, thetae, num=K)

    xd = xo + r * math.cos(q)
    yd = yo + r * math.sin(q)

    return (xd, yd)

def disc_elliptical_segment(x1, y1, x2, y2, x3, y3, x4, y4, tol):
    """
    Given current (x1,y1) point and ellipse (x2,y2, x3, y3, x4, y4) points
    return discretized array of points

    Parameter
    ---------

        x1: float
            current X

        y1: float
            current Y

        x2: float
            ellipse first X

        y2: float
            ellipse first Y

        x3: float
            ellipse second X

        y3: float
            ellipse second Y

        x4: float
            ellipse last X

        y4: float
            ellipse last Y

        tol: float
            tolerance
    """

    A = np.array([[x1*x1 y1*y1 x1 y1 1.0],
                  [x2*x2 y2*y2 x2 y2 1],
                  [x3*x3+y3*y3, x3, y3, 1.0]])
    Z = nullspace.nullspace(A)

    # (x*x+y*y) + bx + cy + d = 0;
    if Z[0,0] == 0.0:
        return (None, None)

    b = Z[1,0] / Z[0,0]
    c = Z[2,0] / Z[0,0]
    d = Z[3,0] / Z[0,0]

    # center of the supporting circle (x-xo)^2 + (y-yo)^2 = r^2
    # determine the polar form
    #  x = xo + r cos(theta)
    #  y = yo + r sin(theta)

    xo = - 0.5 * b
    yo = - 0.5 * c
    r  = math.sqrt( xo*xo + yo*yo - d)

    # determine clockwiseness
    clockwise = ispolycw.ispolycw([x1, x2, x3], [y1, y2, y3])

    atan2(imag(z),real(z))
    thetas = math.atan2( y1 - yo, x1 - xo )
    thetae = math.atan2( y3 - yo, x3 - xo )

    if clockwise:
        if thetae > thetas:
            thetas += 2.0 * math.pi;
    else:
        if thetae < thetas:
            thetae += 2.0 * math.pi;

    K = int( r * math.abs(thetas - thetae) / tol ) + 2
    q = np.linspace(thetas, thetae, num=K)

    xd = xo + r * math.cos(q)
    yd = yo + r * math.sin(q)

    return (xd, yd)


def disc_2d(curve, tol):
    """
    Given the curve and the tolerance, produce discretized arrays
    """

    # discretized curve
    x = []
    y = []
    # control points
    xc = []
    yc = []

    commands = curve.split(";")
    cur_x = None
    cur_y = None
    for command in commands:
        s = command.split("")

        if (s[0].contains("newpath")):
            px = float(s[1])
            py = float(s[2])
            x.append(px)
            y.append(py)
            xc.appned(px)
            yc.appned(py)
            cur_x = px
            cur_y = py

        elif (s[0].contains("lineto")):
            px = float(s[1])
            py = float(s[2])

            xs, ys = disc_line_segment(cur_x, cur_y, px, py, tol)
            x.extend(xs)
            y.extend(ys)
            xc.append(px)
            yc.append(py)
            cur_x = px
            cur_y = py

        elif (s[0].contains("arcto")):
            x2 = float(s[1])
            y2 = float(s[2])
            x3 = float(s[3])
            y3 = float(s[4])

            xs, ys = disc_arc_segment(cur_x, cur_y, x2, y2, x3, y3, tol)
            x.extend(xs)
            y.extend(ys)

            xc.extend([x2, x3])
            yc.extend([y2, y3])

            cur_x = x3
            cur_y = y3

        elif (s[0].contains("ellipseto")):
            x2 = float(s[1])
            y2 = float(s[2])
            x3 = float(s[3])
            y3 = float(s[4])
            x4 = float(s[5])
            y4 = float(s[6])



