# -*- coding: utf-8 -*-

import os
import logging

from XcMath import conversion
from XcIO   import names_helper

def write_input(wrk_dir, template, full_prefix, cl, shot):
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
    """

    logging.info("Start making EGS input")
    logging.debug(wrk_dir)
    logging.debug(template)
    logging.debug(full_prefix)
    logging.debug(str(cl))

    lines = []
    with open(template, "rt") as f:
        lines = f.readlines()

    lines[0] = full_prefix + ";" + "SPAD=18cm;SAD=36cm" + "                                             #!GUI1.0\n"

    # alter phase space file name
    lines[2] = os.path.join(wrk_dir, full_prefix + names_helper.EGSPHAN_EXT + "\n")

    # making source input line with isocenter
    X = 0.0
    Y = shot[0]
    Z = shot[1]
    src = lines[5].split(",")
    fmt = "{0},{1}, {2}, {3}, {4},{5},{6},{7},{8},{9},{10},{11},{12}" # format to put it back
    # replace iso center with user defined shot, in cm
    lines[5] = fmt.format(src[0], src[1], conversion.mm2cm(X), conversion.mm2cm(Y), conversion.mm2cm(Z), src[5], src[6], src[7], src[8], src[9], src[10], src[11], src[12])

    lines[43] = str(cl) + names_helper.EGSPHSF_EXT + "\n"

    fname = os.path.join(wrk_dir, names_helper.make_egsinput_name(full_prefix))
    with open(fname, "wt") as f:
        f.writelines(lines)

    logging.info("Done making EGS input")
    logging.debug(fname)

    return fname

