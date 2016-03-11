import math

def disc_line_segment():
    """
    """

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
    for command in commands:
        s = command.split("")
        if (s[0].contains("newpath")):
            px = float(s[1])
            px = float(s[1])
        elif (s[0].contains("newpath")):