#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import shutil
import subprocess
import time

def ReadPodsToBeDeleted(fname):
    """
    self explanatory
    """

    listPods = []

    with open(fname,'r') as f:
        for line in f:
            listPods.append(line.rstrip('\n'))

    return listPods

# array with replacements
replc = {"r":"R", "c":"C", "x":"X", "y":"Y", "z":"Z", "o":"O", "i":"I", "l":"L", "-":"_", "0":"0", "1":"1", "2":"2","3":"3", "4":"4", "5":"5", "6":"6", "7":"7", "8":"8", "9":"9"}

def normalize_pod(pod):
    """
    Given the pod in Kuberbetes format, normalize it into EGS format
    """

    q = "".join(map(lambda x: replc[x], pod))
    return q

def main(pods_fname):
    """
    This method takes list of pods and delte them all,
    one by one
    """

    pods = ReadPodsToBeDeleted(pods_fname)

    print("To remove PODs: {0}".format(len(pods)))

    for pod in pods:
        thepod = normalize_pod(pod)
        cmd = "kubectl delete pod " + pod
        rc = 0
        for k in range(0, 12): # several attempts to make a pod
            rc = subprocess.call(cmd, shell=True)
            if rc == 0:
                break

        if rc != 0:
            print("Cannot delete pod {0}".format(thepod))
            sys.exit(1)

if __name__ =='__main__':
    nof_args = len(sys.argv)

    if nof_args == 1:
        print("Use:deletePods list_of_PODs")
        sys.exit(1)

    pods_fname = ""
    if nof_args >= 2:
        pods_fname = sys.argv[1]

    main(pods_fname)

    sys.exit(0)

