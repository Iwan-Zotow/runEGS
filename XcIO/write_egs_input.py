# -*- coding: utf-8 -*-

import os
import logging

from XcMath import conversion
from XcIO   import names_helper

def find_egsphsp1(lines):
    """
    """
    k = 0
    for l in lines:
        if names_helper.EGSPHSF_EXT in l:
            return k
        k += 1

    return -1

def write_input(wrk_dir, template, full_prefix, cl, shot, nof_tracks):
    """
    Write EGS input file from template

    Parameters
    ----------

    wrk_dir: string
        working directory

    template: string
        tempalte file name

    full_prefix: string
        full name without extention

    cl: collimator
        collimator used in computation

    shot: tuple of two floats
        shot position, (Y,Z) in MM

    nof_tracks: integer
        number of tracks to run
    """

    logging.info("Start making EGS input")
    logging.debug(wrk_dir)
    logging.debug(template)
    logging.debug(full_prefix)
    logging.debug(str(cl))
    logging.debug(str(shot))
    logging.debug(str(nof_tracks))

    lines = []
    with open(template, "rt") as f:
        lines = f.readlines()

    phsf_pos = find_egsphsp1(lines)
    if phsf_pos < 0:
        raise RuntimeError("no egsphsp1 position in template")

    lines[0] = full_prefix + ";" + "SPAD=18cm;SAD=36cm" + "                                             #!GUI1.0\n"

    # alter EGS phantom file name
    lines[2] = os.path.join(wrk_dir, full_prefix + names_helper.EGSPHAN_EXT + "\n")

    # making source input line with isocenter
    X = 0.0
    Y = shot[0]
    Z = shot[1]
    src = lines[5].split(",")
    fmt = "{0},{1}, {2}, {3}, {4},{5},{6},{7},{8},{9},{10},{11},{12}" # format to put it back
    # replace iso center with user defined shot, in cm
    lines[5] = fmt.format(src[0], src[1], conversion.mm2cm(X), conversion.mm2cm(Y), conversion.mm2cm(Z), src[5], src[6], src[7], src[8], src[9], src[10], src[11], src[12])

    # making phsf file input
    lines[phsf_pos] = str(cl) + names_helper.EGSPHSF_EXT + "\n"

    # making #tracks file input

    lines[phsf_pos+1] = "{0}, 0, 99, 97, 33, 8, 1, 0, 1, 0, , -1, 0, 0, 1, 0\n".format(nof_tracks)

    fname = os.path.join(wrk_dir, names_helper.make_egsinput_name(full_prefix))
    with open(fname, "wt") as f:
        f.writelines(lines)

    logging.info("Done making EGS input")
    logging.debug(fname)

    return fname
