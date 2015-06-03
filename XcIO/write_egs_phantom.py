# -*- coding: utf-8 -*-
"""
Created on Mon Jun 01 15:36:58 2015

@author: Oleg.Krivosheev
"""

import conversion

def write_materials(f, materials):
    """
    Write materials into external stream
    
    Parameters
    ----------

    f: stream
        output stream

    materials: dictionary
        dictionary of materials, id vs tuple (name, density)    
    """
    
    f.write(len(materials))
    for k in range(0, len(materials)):
        f.write(materials[k][0])
        
    f.write("0.000 0.000 0.000 0.000")

def write_boundary(f, bnd):
    """
    Write boundaries into external stream
    
    Parameters
    ----------

    f: stream
        output stream

    bnd: array
        boundaries, in mm
    """

    f.write(len(bnd))
    s = ""
    for b in bnd:
        bcm = conversion.mm2cm(b)
        s += str(bcm) + " "
        
    f.write(s)

def write_header(f, phntom, materials):
    """
    Write EGS phantom header into external stream
    
    Parameters
    ----------

    f: stream
        output stream
        
    phntom: phantom
        holds boundaries, materials and densities

    materials: dictionary
        dictionary of materials, id vs tuple (name, density)    
    """

    write_materials(f, materials)
    
    write_boundary(f, phntom.bx())
    write_boundary(f, phntom.by())
    write_boundary(f, phntom.bz())    
    
def write_matindeces(f, phntom):
    """
    Write EGS phantom material indices
    
    Parameters
    ----------

    f: stream
        output stream
        
    phntom: phantom
        holds boundaries, materials and densities
    """
    
    nx = phntom.nx()   
    ny = phntom.ny()
    nz = phntom.nz()
    
    data = phntom.data()
    
    for iz in range (0, nz):
        for iy in range (0, ny):
            s = ""            
            for ix in range (0, nx):
                
                mat = data[ix,iy,iz]
                s += str(mat)
                
            f.writeline(s)
            
        f.writeline("")

def write_densities(f, phntom):
    """
    Write EGS phantom densities
    
    Parameters
    ----------

    f: stream
        output stream
        
    phntom: phantom
        holds boundaries, materials and densities
    """
    
    nx = phntom.nx()   
    ny = phntom.ny()
    nz = phntom.nz()
    
    dens = phntom.data()

    for iz in range (0, nz):
        for iy in range (0, ny):
            s = ""            
            for ix in range (0, nx):
                
                rho = dens[ix,iy,iz]
                s += str(rho) + " "
                
            f.writeline(s)
            
        f.writeline("")
    
def write_phantom(fname, phntom, materials):
    """
    Write EGS phantom data
    
    Parameters
    ----------

    f: stream
        output stream
        
    phntom: phantom
        holds boundaries, materials and densities
        
    materials: dictionary
        dictionary of materials, id vs tuple (name, density)            
    """
    
    with open(fname, "wt") as f:
        
        write_header(f, phntom, materials)
        write_matindeces(f, phntom)
        write_densities(f, phntom)
