#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

def plot_cup():
    """
    """

    ymin, ymax, zmin, zmax = minmax(dmax)
    #print(ymin, ymax, zmin, zmax)

    step = 5.0
    ny = int( np.around((ymax - ymin)/step) ) + 1
    nz = int( np.around((zmax - zmin)/step) ) + 1
    print(ny, nz)

    sh_dm = np.empty((nz, ny))

    for iz in range(0, nz):
        z = float(iz) * step
        for iy in range(0, ny):
            y = float(iy) * step

            sh_dm[iz, iy] = find_nearby_shot(y, z, dmax)


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

def plot_cup():

    lsof = get_file_list("/home/kriol/data", "R8O1IS01", 25)
    dmax = dmax_all_cups(lsof)

    ymin, ymax, zmin, zmax = minmax(dmax)
    #print(ymin, ymax, zmin, zmax)

    step = 5.0
    ny = int( np.around((ymax - ymin)/step) ) + 1
    nz = int( np.around((zmax - zmin)/step) ) + 1
    print(ny, nz)

    sh_dm = np.empty((nz, ny))

    for iz in range(0, nz):
        z = float(iz) * step
        for iy in range(0, ny):
            y = float(iy) * step

            sh_dm[iz, iy] = find_nearby_shot(y, z, dmax)

    img = None
    fig, axes = plt.subplots(1, 2, figsize=(12, 7), subplot_kw={'xticks': [], 'yticks': []})
    for ax in axes.flat:
        img = ax.imshow(sh_dm, interpolation="none")
        title = "R8O1IS01C25"
        ax.set_title(title)

    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.25, 0.05, 0.5])
    fig.colorbar(img, cax=cbar_ax)

    plt.show()
