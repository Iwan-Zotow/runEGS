#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

polar_angles = [18, 25, 32, 39, 46, 53]

def main(nof_sources):
    """
    Make the middle of EGS template - sources

    nof_sources: int
        Number of sources
    """

    if nof_sources > len(polar_angles):
        raise ValueError("N of sources is too large")

    if nof_sources < 1:
        raise ValueError("N of sources is too small")

    first = 90 - polar_angles[0]
    last  = 90 - polar_angles[nof_sources-1]
    ns    = first - (last - 1)

    print("2, 8, 0, 0, 0, -{}, 18, 180, 0, 180, 0, 0, 0".format(ns))
    delta_phi = 1.0 / float(ns)
    k = 0
    for a in range(first, last-1, -1):
        phi_start = 0.0 + delta_phi*float(k)
        phi_end   = 359.0 + delta_phi*float(k)
        s = "0, {0}, {1:8.6}, {2:.9}, 360, 1".format(a, phi_start, phi_end)
        print(s)
        k += 1

if __name__ == "__main__":
    main(5)
    sys.exit(0)