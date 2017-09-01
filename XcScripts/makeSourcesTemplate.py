# -*- coding: utf-8 -*-

#%%

import os
import sys

POLAR_ANGLES_START = 18
POLAR_ANGLES_TOTAL = 36

def main(nof_sources):
    """
    Make the middle of EGS template - sources

    nof_sources: int
        Number of sources
    """

    if nof_sources > POLAR_ANGLES_TOTAL:
        raise ValueError("N of sources is too large")

    if nof_sources < 1:
        raise ValueError("N of sources is too small, shall be positive")

    first = 90 - POLAR_ANGLES_START
    last  = 90 - (nof_sources + POLAR_ANGLES_START)

    print("2, 8, 0, 0, 0, -{}, 18, 180, 0, 180, 0, 0, 0".format(nof_sources))
    delta_phi = 1.0 / float(nof_sources)
    k = 0
    for a in range(first, last, -1):
        phi_start = 0.0 + delta_phi*float(k)
        phi_end   = 359.0 + delta_phi*float(k)
        s = "0, {0}, {1:8.6}, {2:.9}, 360, 1".format(a, phi_start, phi_end)
        print(s)
        k += 1

if __name__ == "__main__":
    main(25)
    sys.exit(0)
