# -*- coding: utf-8 -*-

import os
import sys
import logging
import multiprocessing

from XcDefinitions import XcConstants
from XcMCCore import clinical
from XcMCCore import qa
from XcMCCore import collimator
from XcIO     import names_helper

import single_shot

def get_clinical_cup():
    """
    Returns tuple with clinical cup description
    """
    return ("8", "2", "M", "01", 25)


def get_clinical_X_range():
    """
    Returns clinical X range
    """
    return (-100.0, 100.0)     # in mm


def get_clinical_Y_range():
    """
    Returns clinical Y range
    """
    return (-100.0, 100.0)     # in mm


def get_clinical_Z_range():
    """
    Returns clinical Z range
    """
    return (-105.0, 100000000.0)     # in mm


def get_clinical_steps():
    """
    Returns clinical steps
    """
    return (1.2, 3.6) # in mm


def get_qa_cup():
    """
    Returns tuple with QA cup description
    """
    # outer cup shall be always 0
    # inner cup shall be always Q
    return ("8", "0", "Q", "00", 25)


def get_qa_X_range():
    """
    Returns qa X range
    """
    return (-80.0, 80.0)     # in mm


def get_qa_Y_range():
    """
    Returns qa Y range
    """
    return (-80.0, 80.0)     # in mm


def get_qa_Z_range():
    """
    Returns qa Z range
    """
    return (0.0, 130.0)     # in mm


def get_qa_steps():
    """
    Returns qa steps
    """
    return (1.0, 2.0) # in mm


def clean_wrk_dir(wrk_dir):
    """
    Clean deep all working directory
    """

    if os.path.isdir(wrk_dir):
        for root, dirs, files in os.walk(wrk_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(wrk_dir)

    return


def run_one_shot(radUnit, outerCup, innerCupSer, innerCupNum, coll, shot, nof_tracks):
    """
    Make everything to compute one shot
    """

    # making working directory
    if not XcConstants.IsQACup(innerCupSer):
        file_prefix = clinical.make_cup_name(radUnit, outerCup, innerCupSer, innerCupNum)
    else:
        file_prefix = qa.make_cup_name(radUnit, outerCup, innerCupSer, innerCupNum)

    full_prefix = names_helper.make_qualified_name(file_prefix, collimator.collimator(coll), shot)

    wrk_dir = os.path.join(os.getcwd(), full_prefix)

    # making empty work dir
    clean_wrk_dir(wrk_dir)
    os.makedirs(wrk_dir)

    # configuring logging
    logging.basicConfig(filename=os.path.join(wrk_dir, full_prefix+".log"), level=logging.DEBUG)
    logging.info("Started")

    logging.info("Running shot for input parameters: {0} {1} {2} {3} {4} {5} {6}".format(radUnit, outerCup, innerCupSer, innerCupNum, coll, shot, nof_tracks) )

    # ranges and steps
    if not XcConstants.IsQACup(innerCupSer):
        x_range = get_clinical_X_range()
        y_range = get_clinical_Y_range()
        z_range = get_clinical_Z_range()

        steps = get_clinical_steps()
    else:
        x_range = get_qa_X_range()
        y_range = get_qa_Y_range()
        z_range = get_qa_Z_range()

        steps = get_qa_steps()

    single_shot.run(wrk_dir, radUnit, outerCup, innerCupSer, innerCupNum, coll, x_range, y_range, z_range, steps, shot, nof_tracks)

    logging.info("Done")


def usage():
    """
    Print use of the main function
    """
    print("Usage: python main.py R8O3IL08C25_Y00Z00 #tracks")


def main():
    """
    Drives all other methods to compute single shot dose
    """

    if len(sys.argv) == 1 or len(sys.argv) == 2:
        # radUnit, outerCup, innerCupSer, innerCupNum, coll = get_clinical_cup() # = get_qa_cup()
        # shot = (0.0, 0.0)
        usage()
        return

    if len(sys.argv) >= 3:
        radUnit, outerCup, innerCupSer, innerCupNum, coll = names_helper.parse_file_prefix(sys.argv[1])
        shot = names_helper.parse_shot(sys.argv[1])
        nof_tracks = int(sys.argv[2])
        if nof_tracks <= 0:
            return

    run_one_shot(radUnit, outerCup, innerCupSer, innerCupNum, coll, shot, nof_tracks)


if __name__ == '__main__':

    main()

    sys.exit(0)
