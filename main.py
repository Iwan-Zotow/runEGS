# -*- coding: utf-8 -*-

"""
Created on Wed May 06 21:11:18 2015

@author: Oleg.Krivosheev
"""

# main routine

import logging
import single_shot
    
def main():
    logging.basicConfig(filename='single_shot.log', level=logging.DEBUG)
    logging.info("Started")
    
    radUnit     = "8"
    outerCup    = "2"
    innerCupSer = "M"
    innerCupNum = "01"

    coll = 25 # in mm

    # ranges
    x_range = (-100.0, 100.0)     # in mm
    y_range = (-100.0, 100.0)     # in mm
    z_range = (-105.0, 1000000.0) # zmax from curve, if lower

    # pair of small and large steps
    steps = (1.2, 6.0) # in mm

    shot = (0.0, 0.0) # in mm
    
    single_shot.run(radUnit, outerCup, innerCupSer, innerCupNum, coll, x_range, y_range, z_range, steps, shot)
    
    logging.info("Done")

if __name__ == '__main__':

    main()
