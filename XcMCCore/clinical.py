# -*- coding: utf-8 -*-

import math

import XcConstants
import phantom
import voxarea

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
    
    return "R" + radUnit + "O" + outerCup + "I" + innerCupSer + innerCupNum
    
def make_phantom(pdim, liA, liB, liC, mats, z_range):
    """
    """
    return make_simple_phantom(pdim, liA, liB, liC, mats, z_range)
    
def make_simple_phantom(pdim, liA, liB, liC, mats, z_range):
    """
    Make phantom given dimensions and curves.
    Pretty much follows original simple design logic
    
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
    
    data = phntom.data()
    dens = phntom.dens()
    
    air   = mats[1]
    water = mats[2]
    ss    = mats[3]    
    poly  = mats[4]
    
    d_air   = air[1]
    d_water = water[1]
    d_ss    = ss[1]
    d_poly  = poly[1]
    
    z_min, z_max = z_range
    
    for iz in range (0, nz):
        z = 0.5 * (bz[iz] + bz[iz+1])

        ra = liA.extrapolate(z)
        rb = liB.extrapolate(z)
        rc = liC.extrapolate(z)
        
        for iy in range (0, ny):
            y = 0.5 * (by[iy] + by[iy+1])
            for ix in range (0, nx):
                x = 0.5 * (bx[ix] + bx[ix+1])

                # default material: air                
                m = 1
                d = d_air
                
                if z <= z_max and z > XcConstants.COUCH_BOTTOM:
                
                    r = math.sqrt(x*x + y*y)
                
                    if r <= ra:
                        m = 2 # water
                        d = d_water
                    elif r <= rb:
                        m = 1 # air
                        d = d_air
                    elif r <= rc:
                        m = 4 # poly
                        d = d_poly
                    else:
                        if not (z <= z_max and z > (XcConstants.COUCH_BOTTOM+XcConstants.COUCH_THICKNESS)):
                            m = 4 # poly
                            d = d_poly
                        
                elif z <= XcConstants.COUCH_BOTTOM:
                    m = 2 # water
                    d = d_water
                
                data[ix,iy,iz] = m
                dens[ix,iy,iz] = d
    
    return phntom
    
def make_complex_phantom(pdim, liA, liB, liC, mats, z_range):
    """
    Make phantom given dimensions and curves.
    Partial voxel volumes
    
    Basic formulas from http://mathworld.wolfram.com/CircularSegment.html
    
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
    
    data = phntom.data()
    dens = phntom.dens()
    
    air   = mats[1]
    water = mats[2]
    ss    = mats[3]    
    poly  = mats[4]
    
    d_air   = air[1]
    d_water = water[1]
    d_ss    = ss[1]
    d_poly  = poly[1]
    
    z_min, z_max = z_range
    
    for iz in range (0, nz):
        z = 0.5 * (bz[iz] + bz[iz+1])

        ra = liA.extrapolate(z)
        rb = liB.extrapolate(z)
        rc = liC.extrapolate(z)
        
        for iy in range (0, ny):
            ymin = by[iy]
            ymax = by[iy+1]
            y = 0.5 * (ymin + ymax)
            for ix in range (0, nx):
                xmin = bx[ix]
                xmax = bx[ix+1]
                x = 0.5 * (xmin + xmax)
                
                # default material: air                
                m = 1
                d = d_air
                
                if z <= z_max and z > XcConstants.COUCH_BOTTOM:
                
                    r = math.sqrt(x*x + y*y)
                
                    if r <= ra:
                        m = 2 # water
                        
                        q = voxarea.vaInner(ra, xmin, xmax, ymin, ymax)                        
                        d = q * d_water + (1.0 - q) * d_air
                        
                    elif r <= rb:
                        m = 1 # air
                        
                        q = voxarea.vaInner(rb, xmin, xmax, ymin, ymax)                        
                        d = q * d_air + (1.0 - q) * d_poly
                        
                    elif r <= rc:
                        m = 4 # poly
                        
                        q = voxarea.vaInner(rc, xmin, xmax, ymin, ymax)                        
                        d = q * d_poly + (1.0 - q) * d_air                        
                    else:
                        if not (z <= z_max and z > (XcConstants.COUCH_BOTTOM+XcConstants.COUCH_THICKNESS)):
                            m = 4 # poly
                            d = d_poly
                        
                elif z <= XcConstants.COUCH_BOTTOM:
                    m = 2 # water
                    d = d_water
                
                data[ix,iy,iz] = m
                dens[ix,iy,iz] = d
    
    return phntom

