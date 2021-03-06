# -*- coding: utf-8 -*-

import os
import json
import logging

import XcConstants
import names_helper
import curve as cc
import collimator
import build_phandim
import cup_downloader
import linint
import materials
import clinical
import qa
import write_egs_phantom
import write_egs_input
import run_dosxyz
import data_uploader

def read_credentials(creds):
    """
    Given the JSON credentials, return tuple with relevant info

    creds: string
        JSON file with credentials

    returns: tuple
        host, port, user, pswd, dest
    """

    logging.info("Reading credentials")
    logging.debug(creds)

    data = None
    with open(creds) as json_file:
        data = json.load(json_file)

    host = data["host"]
    port = data["port"]
    user = data["user"]
    pswd = data["pswd"]
    dest = data["dest"]

    logging.info("Done Reading credentials")

    return (host, port, user, pswd, dest)

def run(wrk_dir, radUnit, outerCup, innerCupSer, innerCupNum, coll, x_range, y_range, z_range, steps, shot):
    """
    Run single shot for a given cup, collimator, shot
    """

    logging.info("Single shot run")
    logging.debug(wrk_dir)
    logging.debug(radUnit)
    logging.debug(outerCup)
    logging.debug(innerCupSer)
    logging.debug(innerCupNum)
    logging.debug(str(coll))
    logging.debug(str(x_range))
    logging.debug(str(y_range))
    logging.debug(str(z_range))
    logging.debug(str(steps))
    logging.debug(str(shot))

    mats = materials.materials("Materials.txt")

    logging.info("Materials initialized")

    cl = collimator.collimator(coll)

    if not XcConstants.IsQACup(innerCupSer):
        file_prefix = clinical.make_cup_name(radUnit, outerCup, innerCupSer, innerCupNum)
    else:
        file_prefix = qa.make_cup_name(radUnit, outerCup, innerCupSer, innerCupNum)

    liA = None
    liB = None
    liC = None
    if not XcConstants.IsQACup(innerCupSer):
        #cdown = cup_downloader.cup_downloader("192.168.1.217", "./", wrk_dir, file_prefix, "kriol", "Proton31")
        cdown = cup_downloader.cup_downloader("192.168.1.230", "/Programs_n_Docs/Kdd_CupGeometry/Out/", wrk_dir, file_prefix, "beamuser", "beamuser")
        cdown.load()
        #cdown.load()
        if (cdown.rc() != 0):
            raise RuntimeError("run_single_shot", "unable to load files")

        logging.info("Cups downloaded")

        cupA = cc.curve(os.path.join( wrk_dir, file_prefix + "_" + "KddCurveA.txt"))
        cupB = cc.curve(os.path.join( wrk_dir, file_prefix + "_" + "KddCurveB.txt"))
        cupC = cc.curve(os.path.join( wrk_dir, file_prefix + "_" + "KddCurveC.txt"))

        liA = linint.linint(cupA)
        liB = linint.linint(cupB)
        liC = linint.linint(cupC)

        logging.info("Interpolators done")

    if not XcConstants.IsQACup(innerCupSer):
        nr = int(cl.size()*1.2/steps[0])
    else:
        nr = int(40.0/steps[0])

    z_max = z_range[1]
    if not XcConstants.IsQACup(innerCupSer):
        z_max = liA.zmax() # z_max = max(liA.zmax(), liB.zmax(), liC.zmax())

    # phantom dimensions and boundaries
    pdim = build_phandim.build_phandim(shot, x_range, y_range, (z_range[0], z_max), steps, nr)

    logging.info("Phantom dimensions")

    # phantom in memory
    if not XcConstants.IsQACup(innerCupSer):
        phntom = clinical.make_phantom(pdim, liA, liB, liC, mats, (z_range[0], z_max))
    else:
        phntom = qa.make_phantom(pdim, liA, liB, liC, mats, (z_range[0], z_max))

    full_prefix = names_helper.make_qualified_name(file_prefix, cl, shot)

    write_egs_phantom.write_phantom(wrk_dir, full_prefix, phntom, mats)

    logging.info("Phantom saved")

    egsinp_template = None
    if not XcConstants.IsQACup(innerCupSer):
        egsinp_template = "template.egsinp"
    else:
        egsinp_template = "templateQA.egsinp"

    egsinp_name = write_egs_input.write_input(wrk_dir, egsinp_template, full_prefix, cl, shot)

    logging.info("Making EGS input")

    logging.info("And DosXYZ is about to run")

    rc = run_dosxyz.run_dosxyz(wrk_dir, egsinp_name, "700jin.pegs4dat")
    if rc != 0:
        logging.info("DosXYZ error: {0}".format(rc))
        raise RuntimeError("run_single_shot", "Dose was not computed")
    logging.info("And DosXYZ is done")

    logging.info("Data uploader is going up")
    logging.info("...right now, no upload")

    host, port, user, pswd, dest = read_credentials("config_sftp.json")
    dupload = data_uploader.data_uploader(wrk_dir, host, port, dest, file_prefix, user, pswd)

    dupload.upload(cl)

    rc = dupload.rc()

    if (rc != 0):
        logging.info("Data upload failure {0}", rc)
        raise RuntimeError("run_single_shot", "unable to upload files")

    logging.info("Data uploaded")
    logging.info("Finita la comedia")
