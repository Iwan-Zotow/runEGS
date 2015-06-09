# -*- coding: utf-8 -*-

import logging
import single_shot

def get_clinical_cup():
    """
    Returns tuple with clinical cup description
    """
    return ("8", "2", "M", "01")
    
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
    return (1.2, 6.0) # in mm

def get_qa_cup():
    """
    Returns tuple with QA cup description
    """
    # outer cup shall be always 0
    # inner cup shall be always Q
    return ("8", "0", "Q", "00")
    
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
    return (1.0, 6.0) # in mm    

def main():
    """
    """
    logging.basicConfig(filename='single_shot.log', level=logging.INFO)
    logging.info("Started")
    
    radUnit, outerCup, innerCupSer, innerCupNum = get_clinical_cup()
    #radUnit, outerCup, innerCupSer, innerCupNum = get_qa_cup()

    coll = 25 # in mm    

    # ranges
    x_range = get_clinical_X_range()
    y_range = get_clinical_Y_range()
    z_range = get_clinical_Z_range()

    # pair of small and large steps
    steps = get_clinical_steps()

    shot = (0.0, 0.0) # in mm
    
    single_shot.run(radUnit, outerCup, innerCupSer, innerCupNum, coll, x_range, y_range, z_range, steps, shot)
    
    logging.info("Done")

if __name__ == '__main__':

    main()
