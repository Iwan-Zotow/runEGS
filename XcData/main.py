#!/usr/bin/python
# -*- coding: utf-8 -*-

import process_set

if __name__ == "__main__":
    # set it to False if you want the default behaviour
    symmetrizeY = True

    process_set.process_set("/home/sphinx/gcloud", "R8O1IS", 1, 9,  "OutYZ", 116.0, symmetrizeY)
    process_set.process_set("/home/sphinx/gcloud", "R8O2IM", 1, 10, "OutYZ", 140.0, symmetrizeY)
    process_set.process_set("/home/sphinx/gcloud", "R8O3IL", 1, 9,  "OutYZ", 153.0, symmetrizeY)
    process_set.process_set("/home/sphinx/gcloud", "R8O0IQ", 0, 0,  "OutYZ",  15.0, symmetrizeY)
