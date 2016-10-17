# -*- coding: utf-8 -*-

import os
import sys
import subprocess

def ReadKddsToBeCalculated(fname):
    """
    self explanatory
    """

    listKdds=[]

    with open(fname,'r') as f:
        for line in f:
            listKdds.append(line.rstrip('\n'))

    return listKdds

gcr = "us.gcr.io"
project = "direct-disk-101619"
docker = "egs-rc-4039"

Kdds = ReadKddsToBeCalculated(sys.argv[1])

docker2run = os.path.join(gcr, project, docker) # full path to docker

for kdd in Kdds:
    cmd = "docker run {0} python main.py {1}".format(docker2run, kdd)
    #print(cmd)
    rc = subprocess.call(cmd, shell=True)
    #print(rc)

