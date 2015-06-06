# -*- coding: utf-8 -*-

import logging

import conversion

def write_materials(f, mats):
    """
    Write materials into external stream
    
    Parameters
    ----------

    f: stream
        output stream

    materials: dictionary
        dictionary of materials, id vs tuple (name, density)    
    """
    
    logging.info("building one boundary")
    
    f.write(" {0}\n".format(len(mats)-1))
    
    for k in range(1, len(mats)):
        f.write(mats[k][0] + "\n")
        
    s = ""
    for k in range(1, len(mats)):
        s += "       0.0000000"
    f.write(s)
    f.write("\n")

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

    s = ""
    for b in bnd:
        bcm = conversion.mm2cm(b)
        s += " {0:.2f}".format(bcm)
        
    f.write(s + "\n")

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
    
    f.write("  {0}  {1}  {2}\n".format(phntom.nx(), phntom.ny(), phntom.nz()))
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
                
            f.write(s)
            f.write("\n")
            
        f.write("\n")

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
    
    dens = phntom.dens()

    for iz in range (0, nz):
        for iy in range (0, ny):
            s = ""            
            for ix in range (0, nx):
                
                rho = dens[ix,iy,iz]
                s += " {0:.7f}".format(rho)
                
            f.write(s)
            f.write("\n")
            
        f.write("\n")
    
def write_phantom(fname, phntom, mats):
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
        
        write_header(f, phntom, mats)
        write_matindeces(f, phntom)
        write_densities(f, phntom)        
