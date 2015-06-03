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
    
    cdown = cup_downloader.cup_downloader("127.0.0.1", "/.", cup_dir, fname_prefix, "kriol", "Proton31")
    cdown.load()
    if (cdown.rc() != 0):
        raise RuntimeError("run_single_shot", "unable to load files")

    return

    cupA = cc.cup_curve(path.join( cup_dir, fname_prefix + "_" + "KddCurveA.txt"))
    cupB = cc.cup_curve(path.join( cup_dir, fname_prefix + "_" + "KddCurveB.txt"))
    cupC = cc.cup_curve(path.join( cup_dir, fname_prefix + "_" + "KddCurveC.txt"))

    liA = linint.linint(cupA)
    liB = linint.linint(cupB)
    liC = linint.linint(cupC)

    nr = int(cl.size()*1.2)

    pdim = build_phandim.build_phandim(shot, x_range, y_range, z_range, steps, nr)
    
    phntom = make_phantom(pdim, liA, liB, liC, mats)
    
    egsphname = path.join(out_dir, fname_prefix + str(cl) + ".egsphant")
    
    write_egs_phantom.write_phantom(egsphname, phntom, materials)
    
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
    # ss    = mats[3]    
    poly  = mats[4]
    
    for iz in range (0, nz):
        z = 0.5 * (bz[iz].x() + bz[iz+1].x())
        for iy in range (0, ny):
            y = 0.5 * (by[iy].x() + by[iy+1].x())    
            for ix in range (0, nx):
                x = 0.5 * (bx[ix].x() + bx[ix+1].x())
                
                r = math.sqrt(x*x + y*y)
                
                ra = liA.interpolate(z)
                
                if r <= ra:
                    data[ix,iy,iz] = 2 # water
                    dens[ix,iy,iz] = water[1]
                    continue
                    
                rb = liB.interpolate(z)
                
                if r <= rb:
                    data[ix,iy,iz] = 1 # air
                    dens[ix,iy,iz] = air[1]
                    continue
                
                rc = liC.interpolate(z)

                if r <= rc:
                    data[ix,iy,iz] = 4 # poly
                    dens[ix,iy,iz] = poly[1]
                    continue
    
    return phntom
