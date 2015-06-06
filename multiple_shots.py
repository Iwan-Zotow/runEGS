# -*- coding: utf-8 -*-

import path

import names_helper
import curve as cc
import collimator
import build_phandim
import cup_downloader
import linint
import materials
import clinical
import write_egs_phantom
import write_egs_input
import run_dosxyz
import data_uploader

def make_shot_list(radUnit, outerCup, innerCupSer, innerCupNum, coll, x_range, y_range, z_range, shstep, shmargin):
    """
    """
    
    cl = collimator.collimator(coll)

    file_prefix = clinical.make_cup_name(radUnit, outerCup, innerCupSer, innerCupNum)
    
    #cdown = cup_downloader.cup_downloader("127.0.0.1", cup_dir, "/.", file_prefix, "kriol", "Proton31")
    #cdown.load()
    # if (cdown.rc() != 0):
    #     raise RuntimeError("run_single_shot", "unable to load files")

    cupA = cc.curve(path.join( cup_dir, file_prefix + "_" + "KddCurveA.txt"))
    
    liA = linint.linint(cupA)
    
    z_max = liA.zmax()
    
    ny_min = int(y_range[0] / shstep) - 1
    ny_max = int(y_range[1] / shstep) + 1    
    
    nz_min = int(z_range[0] / shstep) - 1
    nz_max = int(z_max / shstep) + 1
    
    shots = []
    for iy in range(ny_min, ny_max):
        y = shstep * float(iy)
        for iz in range(nz_min, nz_max):
            z = shstep * float(iz)
            
            r = liA.extrapolate(z)
            
            if y < r: # we're inside the inner cup
                shot = (y, z)
                shots.append(shot)
                
    return shots
