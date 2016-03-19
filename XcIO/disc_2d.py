#
# This module is about discretization of different 2d elements
# For a given element and tolerance it produces set of
# discretized (x,y) points
#

import math
import numpy as np

from XcMath import nullspace
from XcMath import ispolycw

def disc_line_segment(xs, ys, xe, ye, tol):
    """
    Given start (x,y) point and end (x,y) point
    return discretized array of points

    Parameter
    ---------

        xs: float
            start X

        ys: float
            start Y

        xe: float
            end X

        ye: float
            end Y

        tol: float
            tolerance
    """

    x = []
    y = []

    if xs == None or ys == None:
        return (None, None)
    if xe == None or ye == None:
        return (None, None)

    d = math.sqrt((xe - xs)**2 + (ye - ys)**2)
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
    clockwise, area = ispolycw.ispolycw([x1, x2, x3], [y1, y2, y3])

    thetas = math.atan2( y1 - yo, x1 - xo )
    thetae = math.atan2( y3 - yo, x3 - xo )

    if clockwise:
        if thetae > thetas:
            thetas += 2.0 * math.pi
    else:
        if thetae < thetas:
            thetae += 2.0 * math.pi

    K = int( r * math.fabs(thetas - thetae) / tol ) + 2
    q = np.linspace(thetas, thetae, num=K)

    xd = xo + r * np.cos(q)
    yd = yo + r * np.sin(q)

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

    A = np.array([[x1*x1, y1*y1, x1, y1, 1.0],
                  [x2*x2, y2*y2, x2, y2, 1.0],
                  [x3*x3, y3*y3, x3, y3, 1.0],
                  [x4*x4, y4*y4, x4, y4, 1.0]])
    Z = nullspace.nullspace(A)

    # Z(0)*x**2 + Z(1)*y**2 + Z(2)*x + Z(3)*y + Z(4) = 0
    if Z[0,0] == 0.0:
        return (None, None)
    if Z[1,0] == 0.0:
        return (None, None)
    if Z[0,0]*Z[1,0] < 0.0: # sign check
        return (None, None)

    # convert to (x-xo)^2/a^2 + (y-yo)^2/b^2 = 1
    xo = -0.5 * Z[2, 0] / Z[0, 0]
    yo = -0.5 * Z[3, 0] / Z[1, 0]

    a = math.sqrt( (Z[0, 0]*xo*xo + Z[1, 0]*yo*yo - Z[4, 0])/Z[0, 0] )
    b = math.sqrt( (Z[0, 0]*xo*xo + Z[1, 0]*yo*yo - Z[4, 0])/Z[1, 0] )

    # determine clockwiseness
    clockwise = ispolycw.ispolycw([x1, x2, x3], [y1, y2, y3])
    if clockwise != ispolycw.ispolycw([x2, x3, x4], [y2, y3, y4]): # check all points
        return (None, None)

    thetas = math.atan2( (y1 - yo)/b, (x1 - xo)/a )
    thetae = math.atan2( (y4 - yo)/b, (x4 - xo)/a )

    if clockwise:
        if thetae > thetas:
            thetas += 2.0 * math.pi
    else:
        if thetae < thetas:
            thetae += 2.0 * math.pi

    K = int( math.sqrt( a*a + b*b ) * math.fabs(thetas - thetae) / tol ) + 2
    q = np.linspace(thetas, thetae, num=K)

    xd = xo + a * np.cos(q)
    yd = yo + b * np.sin(q)

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

    commands = curve.split(";") # get list of separate commands
    cur_x = None
    cur_y = None
    for command in commands:
        s = command.split(" ")
        s = [q for q in s if q] # remove empty strings

        cmd = s[0]

        if "newpath" in cmd:
            px = float(s[1])
            py = float(s[2])
            x.append(px)
            y.append(py)
            xc.append(px)
            yc.append(py)
            cur_x = px
            cur_y = py

        elif "lineto" in cmd:
            px = float(s[1])
            py = float(s[2])

            xs, ys = disc_line_segment(cur_x, cur_y, px, py, tol)
            x.extend(xs)
            y.extend(ys)
            xc.append(px)
            yc.append(py)
            cur_x = px
            cur_y = py

        elif "arcto" in cmd:
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

        elif "ellipseto" in cmd:
            x2 = float(s[1])
            y2 = float(s[2])
            x3 = float(s[3])
            y3 = float(s[4])
            x4 = float(s[5])
            y4 = float(s[6])

            xs, ys = disc_elliptical_segment(cur_x, cur_y, x2, y2, x3, y3, x4, y4, tol)
            x.extend(xs)
            y.extend(ys)

            xc.extend([x2, x3, x4])
            yc.extend([y2, y3, y4])

            cur_x = x4
            cur_y = y4

        elif "closepath" in cmd:
            break

        else:
            raise RuntimeError("disc_2d::unknown command {0}".format(cmd))

    return (np.asarray(x), np.asarray(y), np.asarray(xc), np.asarray(yc))

if __name__ == "__main__":

    xs, ys = disc_line_segment(0.0, 0.0, 1.0, 1.0, 0.05)
    for x, y in map(lambda x, y: (x,y), xs, ys):
        print(x, y)

    print("========================")

    xs, ys = disc_arc_segment(0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.05)
    for x, y in map(lambda x, y: (x,y), xs, ys):
        print(x, y)

    print("========================")

    xs, ys = disc_elliptical_segment(0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 2.0, -1.0, 0.05)
    print(xs)
    print(ys)

    if xs != None and ys != None:
        for x, y in map(lambda x, y: (x,y), xs, ys):
            print(x, y)
