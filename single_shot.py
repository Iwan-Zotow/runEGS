from os import path
import math

import curve as cc
import phantom
import collimator
import build_phandim
import cup_downloader
import linint
import materials
import write_egs_phantom
import write_egs_input
import run_dosxyz
import data_uploader

def run(radUnit, outerCup, innerCupSer, innerCupNum, coll, x_range, y_range, z_range, steps, shot):
    """
    Run single shot for a given cup, collimator, shot
    """
    
    cup_dir = "cup_geometry"
    out_dir = "cup_egsphan"

    mats = materials.materials("Materials.txt")

    cl = collimator.collimator(coll)

    fname_prefix = make_cup_name(radUnit, outerCup, innerCupSer, innerCupNum)
    
    #cdown = cup_downloader.cup_downloader("127.0.0.1", cup_dir, "/.", fname_prefix, "kriol", "Proton31")
    #cdown.load()
    # if (cdown.rc() != 0):
    #     raise RuntimeError("run_single_shot", "unable to load files")

    cupA = cc.curve(path.join( cup_dir, fname_prefix + "_" + "KddCurveA.txt"))
    cupB = cc.curve(path.join( cup_dir, fname_prefix + "_" + "KddCurveB.txt"))
    cupC = cc.curve(path.join( cup_dir, fname_prefix + "_" + "KddCurveC.txt"))    
    
    liA = linint.linint(cupA)
    liB = linint.linint(cupB)
    liC = linint.linint(cupC)

    nr = int(cl.size()*1.2/steps[0])

    z_max = liA.zmax() # z_max = max(liA.zmax(), liB.zmax(), liC.zmax())

    pdim = build_phandim.build_phandim(shot, x_range, y_range, (z_range[0], z_max), steps, nr)
    
    fname = fname_prefix + str(cl)
    fname = fname + "_" + "Y{0}Z{1}".format(int(shot[0]),int(shot[1])) + ".egsphant"
    egsphname = path.join(out_dir, fname)
    
    phntom = make_phantom(pdim, liA, liB, liC, mats)
    
    write_egs_phantom.write_phantom(egsphname, phntom, mats)
    
    return
    
    egnsinp_name = write_egs_input.write_input("template.egsinp", fname_prefix, coll, shot)
    
    rc = run_dosxyz.run(egnsinp_name, "700jin.pegs4dat")
    if rc != 0:
        raise RuntimeError("run_single_shot", "Dose was not computed")
        
    dupload = data_uploader.data_uploader("127.0.0.1", "/.", fname_prefix, "kriol", "Proton31")
    
    dupload.upload()
    

def make_cup_name(radUnit, outerCup, innerCupSer, innerCupNum):
    """
    Makes filename give RU, OC, IC info
    """
    return "R" + radUnit + "O" + outerCup + "I" + innerCupSer + innerCupNum
    
def make_phantom(pdim, liA, liB, liC, mats):
    """
    Make phantom given dimensions and curves
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
                
                m = 1
                d = d_air
                
                if r <= ra:
                    m = 2 # water
                    d = d_water
                elif r <= rb:
                    m = 1 # air
                    d = d_air
                elif r <= rc:
                    m = 4 # poly
                    d = d_poly
                
                data[ix,iy,iz] = m
                dens[ix,iy,iz] = d
    
    return phntom
