# -*- coding: utf-8 -*-

import os
import sys
import json
import shutil
import subprocess
import time

from XcScripts import readKdds
from XcIO.Kdd_Pod import kdd2pod, pod2kdd

def main(pods_fname):
    """
    This method takes list of pods and delete them all,
    one by one
    """

    pods = readKdds.readKdds(pods_fname)

    print("To remove PODs: {0}".format(len(pods)))

    for pod in pods:
        thepod = kdd2pod(pod)
        cmd = "kubectl delete pod " + thepod
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

