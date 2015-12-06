#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import numpy as np

import read_3ddose
import names_helper

SHOT_X = 0.0

def find_shot_index(b, pos):
    """
    Given boundaries and position, return position index

    Parameters
    ----------

    b: array of floats
        boundaries, mm
    pos: float
        shot 1d position, mm

    returns: boolean
        True if ok, False otherwise
    """
    idx  = -1
    dist = 10000.0
    for k in range(0, len(b)):
        d = math.fabs(pos - b[k])
        if d < dist:
            dist = d
            idx  = k

    return idx

def get_3ddose(top, full_prefix):
    """
    Read and return symmetrized 3ddose

    Parameters
    ----------

    top: string
        top dir location

    full_prefix: string
        name of shot the compressed shot data file

    returns: 3ddose object
        3ddose
    """

    tddose = read_3ddose.read_data(top, full_prefix)

    can_sym_X = tddose.could_sym_x()
    if not can_sym_X:
        raise Exception("Cannot X AVERAGE, bad X boundaries\n")

    tddose.do_sym_x()
    if not tddose.sym_x():
        raise Exception("Something went wrong on X symmetrization\n")

    can_sym_Y = tddose.could_sym_y() # check if we can...

    if can_sym_Y:
        tddose.do_sym_y()
        if not tddose.sym_y():
            raise Exception("Something went wrong on Y symmetrization\n")

    return tddose

def dmax_shot(tddose, shot_y, shot_z):
    """
    Find dmax for a shot

    Parameters
    ----------

    tddose: 3ddose object
        contains dose and boundaries, possible symmetrized

    shot_y: float
        Y shot position, mm

    shot_z: float
        Z shot position, mm

    returns: tuple of shot position and dose
        dose averaged around the shot, using 2x2x2 voxels volume,
        plus shot X, Y and Z positions, in mm
    """

    six = find_shot_index(tddose.bx(), SHOT_X)
    siy = find_shot_index(tddose.by(), float(shot_y))
    siz = find_shot_index(tddose.bz(), float(shot_z))

    data = tddose.data()

    dmax = (data[six  , siy, siz] + data[six  , siy+1, siz] + data[six  , siy, siz+1] + data[six  , siy+1, siz+1] +
            data[six+1, siy, siz] + data[six+1, siy+1, siz] + data[six+1, siy, siz+1] + data[six+1, siy+1, siz+1])/8.0

    return SHOT_X, shot_y, shot_z, dmax

def dmax_curve_x(tddose, shot_y, shot_z):
    """
    Return dmax X curve for a shot

    Parameters
    ----------

    tddose: 3ddose object
        contains dose and boundaries, possible symmetrized

    shot_y: float
        Y shot position, mm

    shot_z: float
        Z shot position, mm

    returns: tuple of array and array, both floats
        dose curve averaged around the shot position, using 2x2 strips,
        boundary array, in mm
    """

    six = find_shot_index(tddose.bx(), SHOT_X)
    siy = find_shot_index(tddose.by(), float(shot_y))
    siz = find_shot_index(tddose.bz(), float(shot_z))

    curve = ( data[:, siy, siz  ] + data[:, siy+1, siz  ] +
              data[:, siy, siz+1] + data[:, siy+1, siz+1]  )/4.0

    return (tddose.bx(), curve)

def dmax_curve_y(tddose, shot_y, shot_z):
    """
    Return dmax Y curve for a shot

    Parameters
    ----------

    tddose: 3ddose object
        contains dose and boundaries, possible symmetrized

    shot_y: float
        Y shot position, mm

    shot_z: float
        Z shot position, mm

    returns: tuple of array and array, both floats
        dose curve averaged around the shot position, using 2x2 strips,
        boundary array, in mm
    """

    six = find_shot_index(tddose.bx(), SHOT_X)
    siy = find_shot_index(tddose.by(), float(shot_y))
    siz = find_shot_index(tddose.bz(), float(shot_z))

    curve = ( data[six, :, siz  ] + data[six + 1, :, siz  ] +
              data[six, :, siz+1] + data[six + 1, :, siz+1]  )/4.0

    return (tddose.by(), curve)

def dmax_curve_z(tddose, shot_y, shot_z):
    """
    Return dmax Z curve for a shot

    Parameters
    ----------

    tddose: 3ddose object
        contains dose and boundaries, possible symmetrized

    shot_y: float
        Y shot position, mm

    shot_z: float
        Z shot position, mm

    returns: tuple of array and array, both floats
        dose curve averaged around the shot position, using 2x2 strips,
        boundary array, in mm
    """

    six = find_shot_index(tddose.bx(), SHOT_X)

    siy = find_shot_index(tddose.by(), float(shot_y))
    siz = find_shot_index(tddose.bz(), float(shot_z))

    curve = ( data[six, siy  , :] + data[six + 1, siy  , :] +
              data[six, siz+1, :] + data[six + 1, siy+1, :]  )/4.0

    return (tddose.bz(), curve)

def calc_window_left(b, d, v):
    """
    For a given value of v, calculate left window position on the curve

    Parameters
    ----------

    b: array of floats
        boundaries, in mm

    d: array of floats
        data/dose array, length is one less than boundaries

    v: float
        value for position to be found

    returns: float
        left window position, mm. NaN if unsuccessful
    """

    if v <= d[0]:
        step = 0.5 * (b[1] - b[0])
        x    = (b[0] - s) + v*2.0*step/d[0]
        return x

    for k in range(1, len(d)):
        if v <= d[k]:
            x_k1 = 0.5*(b[k-1] + b[k])
            x_k  = 0.5*(b[k] + b[k+1])
            p = (v - d[k-1]) / (d[k] - d[k-1])
            x = x_k1 + p*(x_k - x_k1)
            return x

    return np.nan

def calc_window_right(b, d, v):
    """
    For a given value of v, calculate right window position on the curve

    Parameters
    ----------

    b: array of floats
        boundaries, in mm

    d: array of floats
        data/dose array, length is one less than boundaries

    v: float
        value for position to be found

    returns: float
        right window position, mm. NaN if unsuccessful
    """

    return calc_window_right(b[::-1], d[::-1], v)

def calc_window(b, d, v):
    """
    for a given value of v, calculate left and right position on the curve

    Parameters
    ----------

    b: array of floats
        boundaries, in mm

    d: array of floats
        data array, length is one less than boundaries

    v: float
        value to be found

    returns: tuple of floats
        left and right position
    """

    return (calc_window_left(b, d, v), calc_window_right(b, d, v))

def process_shot(top, full_prefix):
    """
    Given the top directory and full prefix,
    return essential info about the shot
    """

    shot_y, shot_z = names_helper.parse_shot( full_prefix )

    tddose = get_3ddose(top, full_prefix)

    dm = dmax_shot(tddose, shot_y, shot_z)

    bz, cx = dmax_curve_x(tddose, shot_y, shot_z)
    by, cy = dmax_curve_y(tddose, shot_y, shot_z)
    bz, cz = dmax_curve_z(tddose, shot_y, shot_z)

    xw25 = calc_window(bx, cx, 0.25*dm)
    xw50 = calc_window(bx, cx, 0.50*dm)
    xw75 = calc_window(bx, cx, 0.50*dm)

    yw25 = calc_window(by, cy, 0.25*dm)
    yw50 = calc_window(by, cy, 0.50*dm)
    yw75 = calc_window(by, cy, 0.50*dm)

    zw25 = calc_window(bz, cz, 0.25*dm)
    zw50 = calc_window(bz, cz, 0.50*dm)
    zw75 = calc_window(bz, cz, 0.50*dm)

    return (shot_y, shot_z, dm,
            xw25, xw50, xw75,
            yw25, yw50, yw75,
            zw25, zw50, zw75 )

if __name__ == "__main__":

     ttt = process_shot("/home/kriol/data/R8O1IS01C25", "R8O1IS01C25_Y35Z25")
