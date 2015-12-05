#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import numpy as np
import matplotlib.pyplot as plt

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

def dmax_shot(tddose, full_prefix):
    """
    Find dmax for a shot

    Parameters
    ----------

    tddose: 3ddose object
        contains dose and boundaries, possible symmetrized

    full_prefix: string
        name of shot the compressed shot data file

    returns: tuple of shot position and dose
        dose averaged around the shot, using 2x2x2 voxels volume,
        plus shot X, Y and Z positions, in mm
    """

    shot_y, shot_z = names_helper.parse_shot( full_prefix )

    six = find_shot_index(tddose.bx(), SHOT_X)
    siy = find_shot_index(tddose.by(), float(shot_y))
    siz = find_shot_index(tddose.bz(), float(shot_z))

    data = tddose.data()

    dmax = (data[six  , siy, siz] + data[six  , siy+1, siz] + data[six  , siy, siz+1] + data[six  , siy+1, siz+1] +
            data[six+1, siy, siz] + data[six+1, siy+1, siz] + data[six+1, siy, siz+1] + data[six+1, siy+1, siz+1])/8.0

    return SHOT_X, shot_y, shot_z, dmax

def dmax_curve_x(tddose, full_prefix):
    """
    Return dmax X curve for a shot

    Parameters
    ----------

    tddose: 3ddose object
        contains dose and boundaries, possible symmetrized

    full_prefix: string
        name of shot the compressed shot data file

    returns: tuple of array and array, both floats
        dose curve averaged around the shot position, using 2x2 strips,
        boundary array, in mm
    """

    shot_y, shot_z = names_helper.parse_shot( full_prefix )

    six = find_shot_index(tddose.bx(), SHOT_X)
    siy = find_shot_index(tddose.by(), float(shot_y))
    siz = find_shot_index(tddose.bz(), float(shot_z))

    curve = ( data[:, siy, siz  ] + data[:, siy+1, siz  ] +
              data[:, siy, siz+1] + data[:, siy+1, siz+1]  )/4.0

    return (tddose.bx(), curve)

def dmax_curve_y(tddose, full_prefix):
    """
    Return dmax Y curve for a shot

    Parameters
    ----------

    tddose: 3ddose object
        contains dose and boundaries, possible symmetrized

    full_prefix: string
        name of shot the compressed shot data file

    returns: tuple of array and array, both floats
        dose curve averaged around the shot position, using 2x2 strips,
        boundary array, in mm
    """

    shot_y, shot_z = names_helper.parse_shot( full_prefix )

    six = find_shot_index(tddose.bx(), SHOT_X)
    siy = find_shot_index(tddose.by(), float(shot_y))
    siz = find_shot_index(tddose.bz(), float(shot_z))

    curve = ( data[six, :, siz  ] + data[six + 1, :, siz  ] +
              data[six, :, siz+1] + data[six + 1, :, siz+1]  )/4.0

    return (tddose.by(), curve)

def dmax_curve_z(tddose, full_prefix):
    """
    Return dmax Z curve for a shot

    Parameters
    ----------

    tddose: 3ddose object
        contains dose and boundaries, possible symmetrized

    full_prefix: string
        name of shot the compressed shot data file

    returns: tuple of array and array, both floats
        dose curve averaged around the shot position, using 2x2 strips,
        boundary array, in mm
    """

    shot_y, shot_z = names_helper.parse_shot( full_prefix )
    six = find_shot_index(tddose.bx(), SHOT_X)

    siy = find_shot_index(tddose.by(), float(shot_y))
    siz = find_shot_index(tddose.bz(), float(shot_z))

    curve = ( data[six, siy  , :] + data[six + 1, siy  , :] +
              data[six, siz+1, :] + data[six + 1, siy+1, :]  )/4.0

    return (tddose.bz(), curve)

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

    left = b[0]
    if v > d[0]:


def plot_shot(top, full_prefix):
    """
    Read data, process it and plot it

    Parameters
    ----------

    top: string
        top dir location

    full_prefix: string
        name of shot the compressed shot data file

    returns: 3ddose object
        3d dose grid with boundaries
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

    dose  = tddose.data()
    izmax = tddose.nz()

    bx = tddose.bx()
    by = tddose.bx()

    fig, axes = plt.subplots(6, 6, figsize=(12, 6), subplot_kw={'xticks': [], 'yticks': []})
    fig.subplots_adjust(hspace=0.3, wspace=0.05)

    k = 0
    for ax in axes.flat:
        zidx = 0 + k
        if zidx >= izmax:
            zidx = izmax-1

        plane = dose[:,:,zidx]
        nbx, nby, nplne = read_3ddose.expand_plane(plane, bx, by)

        ax.imshow(nplne, interpolation="none")
        title = "Z idx:{0}".format(zidx)
        ax.set_title(title)

        k += 2

    return tddose

if __name__ == "__main__":

    tddose = plot_shot("/home/kriol/data/R8O1IS01C25", "R8O1IS01C25_Y35Z25")
    #tddose = plot_shot("/home/kriol/data", "R8O1IS01C25_Y0Z0")

    plt.show()
