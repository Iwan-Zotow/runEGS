# -*- coding: utf-8 -*-

import math

import names_helper
from utils import squared
import phantom

# for a moment we use the same scheme for clinical and QA cups
def make_cup_name(radUnit, outerCup, innerCupSer, innerCupNum):
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
    return names_helper.make_cup_prefix(radUnit, outerCup, innerCupSer, innerCupNum)

def make_phantom(pdim, liA, liB, liC, mats, z_range, table = None):
    """
    Make QA phantom given dimensions and curves

    Parameters
    ----------

        pdim: phandim
            phantom dimensions

        liA: linint
            inner cup curve

        liB: linint
            outer cup inner curve

        liC: linint
            outer cup outer curve

        mats: materials
            containes materials

        z_range: (float,float) tuple
            Z coordinates range

        table: table
            table to take into account, if None then it is not here

    returns: phantom
        pahntom filled with materials and densities
    """

    phntom = phantom.phantom(pdim.bx(), pdim.by(), pdim.bz())

    nx = phntom.nx()
    ny = phntom.ny()
    nz = phntom.nz()

    bx = phntom.bx()
    by = phntom.by()
    bz = phntom.bz()

    # denity and material indeces
    idxs = phntom.mats()
    dens = phntom.data()

    air   = mats[1]
    water = mats[2]
    ss    = mats[3]
    poly  = mats[4]
    pmma  = mats[5]

    d_air   = air[1]
    d_water = water[1]
    d_ss    = ss[1]
    d_poly  = poly[1]
    d_pmma  = pmma[1]

    z_min, z_max = z_range

    for iz in range (0, nz):
        z = 0.5 * (bz[iz] + bz[iz+1])
        for iy in range (0, ny):
            y = 0.5 * (by[iy] + by[iy+1])
            for ix in range (0, nx):
                x = 0.5 * (bx[ix] + bx[ix+1])

                # default material: air
                m = 1
                d = d_air

                r = math.sqrt(x*x + y*y)

                # as lifted from qa/make_cups
                # all units are in mm
                if z > 15.0 and z <= 15.0+46.0 and r <= 77.0:
                    m = 5 # PMMA
                    d = d_pmma
                elif z > 15.0+46.0 and z <= 15.0+115.0 and math.sqrt(squared(r)+squared(z-(15.0+46.0))) <= 77.0:
                    m = 5 # PMMA
                    d = d_pmma

                idxs[ix,iy,iz] = m
                dens[ix,iy,iz] = d

    return phntom
