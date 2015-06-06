from os import path

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

def run(radUnit, outerCup, innerCupSer, innerCupNum, coll, x_range, y_range, z_range, steps, shot):
    """
    Run single shot for a given cup, collimator, shot
    """
    
    cup_dir = "cup_geometry"
    out_dir = "." # "cup_egsphan"

    mats = materials.materials("Materials.txt")

    cl = collimator.collimator(coll)

    file_prefix = clinical.make_cup_name(radUnit, outerCup, innerCupSer, innerCupNum)
    
    #cdown = cup_downloader.cup_downloader("127.0.0.1", cup_dir, "/.", file_prefix, "kriol", "Proton31")
    #cdown.load()
    # if (cdown.rc() != 0):
    #     raise RuntimeError("run_single_shot", "unable to load files")

    cupA = cc.curve(path.join( cup_dir, file_prefix + "_" + "KddCurveA.txt"))
    cupB = cc.curve(path.join( cup_dir, file_prefix + "_" + "KddCurveB.txt"))
    cupC = cc.curve(path.join( cup_dir, file_prefix + "_" + "KddCurveC.txt"))    
    
    liA = linint.linint(cupA)
    liB = linint.linint(cupB)
    liC = linint.linint(cupC)

    nr = int(cl.size()*1.2/steps[0])

    z_max = liA.zmax() # z_max = max(liA.zmax(), liB.zmax(), liC.zmax())

    pdim = build_phandim.build_phandim(shot, x_range, y_range, (z_range[0], z_max), steps, nr)
    
    fname = names_helper.make_qualified_name(file_prefix, cl, shot) + names_helper.EGSPHAN_EXT
    egsphname = path.join(out_dir, fname)
    
    phntom = clinical.make_phantom(pdim, liA, liB, liC, mats, (z_range[0], z_max))
    
    write_egs_phantom.write_phantom(egsphname, phntom, mats)
    
    egsinp_name = write_egs_input.write_input("template.egsinp", file_prefix, cl, shot)

    rc = run_dosxyz.run_dosxyz(egsinp_name, "700jin.pegs4dat")
    if rc != 0:
        raise RuntimeError("run_single_shot", "Dose was not computed")

    return
        
    dupload = data_uploader.data_uploader("127.0.0.1", "/.", file_prefix, "kriol", "Proton31")
    
    dupload.upload()


