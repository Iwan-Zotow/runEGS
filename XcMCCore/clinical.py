# -*- coding: utf-8 -*-

import math

import XcConstants
import names_helper
import phantom
import voxarea

EPS = 1.0e-4

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
    
    dens = phntom.data()
    idxs = phntom.mats()
    
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

                r = math.sqrt(x*x + y*y)
                
                # default material: air                
                m = 1
                d = d_air
                
                if z <= z_max and z > XcConstants.COUCH_BOTTOM:
                
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
                
                idxs[ix,iy,iz] = m
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
    
    idxs = phntom.mats()
    dens = phntom.data()
    
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
                
                r = math.sqrt(x*x + y*y)
                    
                # default material: air                
                m = 1
                d = d_air
                
                if z <= z_max and z > XcConstants.COUCH_BOTTOM:
                
                    if r <= ra:
                        m = 2 # water
                        
                        q = voxarea.vaInner(ra, xmin, ymin, xmax, ymax)
                        if q < 0.0 and q > -EPS:
                            q = 0.0
                        if q > 1.0 and q < 1.0+EPS:
                            q = 1.0
                        
                        p = voxarea.vaInner(ra, xmin, ymin, xmax, ymax)
                        if p < 0.0 and p > -EPS:
                            p = 0.0
                        if p > 1.0 and p < 1.0+EPS:
                            p = 1.0
                        
                        w_w = q
                        w_a = p - q
                        w_p = 1.0 - p
                        if w_w < 0.0 or w_w > 1.0 or w_a < 0.0 or w_a > 1.0 or w_p < 0.0 or w_p > 1.0:
                            print("RA: {0} {1} {2}".format(w_W, w_a, w_p))
                                                        
                        d = w_w * d_water + w_a * d_air + w_p * d_poly
                        
                    elif r <= rb:
                        m = 1 # air
                        
                        p = voxarea.vaOuter(ra, xmin, ymin, xmax, ymax)
                        if p < 0.0 and p > -EPS:
                            p = 0.0
                        if p > 1.0 and p < 1.0+EPS:
                            p = 1.0
                            
                        q = voxarea.vaInner(rb, xmin, ymin, xmax, ymax)
                        if q < 0.0 and q > -EPS:
                            q = 0.0
                        if q > 1.0 and q < 1.0+EPS:
                            q = 1.0
                        
                        w_w = p
                        w_a = q - p
                        w_p = 1.0 - q
                        
                        if w_w < 0.0 or w_w > 1.0 or w_a < 0.0 or w_a > 1.0 or w_p < 0.0 or w_p > 1.0:
                            print("RB: {0} {1} {2}".format(w_w, w_a, w_p))
                        d = w_w * d_water + w_a * d_air + w_p * d_poly
                        
                    elif r <= rc:
                        m = 4 # poly
                        
                        p = voxarea.vaOuter(rb, xmin, ymin, xmax, ymax)
                        if p < 0.0 and p > -EPS:
                            p = 0.0
                        if p > 1.0 and p < 1.0+EPS:
                            p = 1.0
                            
                        q = voxarea.vaInner(rc, xmin, ymin, xmax, ymax)
                        if q < 0.0 and q > -EPS:
                            q = 0.0
                        if q > 1.0 and q < 1.0+EPS:
                            q = 1.0
                        
                        w_a = p
                        w_p = q - p
                        w_aa= 1.0 - q
                        if w_a < 0.0 or w_a > 1.0 or w_p < 0.0 or w_p > 1.0 or w_aa < 0.0 or w_aa > 1.0:
                            print("RC: {0} {1} {2}".format(w_a, w_p, w_aa))
                        d = w_a * d_air + w_p * d_poly + w_aa * d_air                        
                    else:
                        if not (z <= z_max and z > (XcConstants.COUCH_BOTTOM+XcConstants.COUCH_THICKNESS)):
                            m = 4 # poly
                            
                            p = voxarea.vaOuter(rc, xmin, ymin, xmax, ymax)
                            if p < 0.0 and p > -EPS:
                                p = 0.0
                            if p > 1.0 and p < 1.0+EPS:
                                p = 1.0
                                
                            if p < 0.0 or p > 1.0:
                                print("RD: {0}".format(p))
                            d = p*d_poly + (1.0-p)*d_air
                        
                elif z <= XcConstants.COUCH_BOTTOM:
                    m = 2 # water
                    d = d_water
                
                idxs[ix,iy,iz] = m
                dens[ix,iy,iz] = d
    
    return phntom
