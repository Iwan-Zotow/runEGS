#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import shutil
import subprocess
import time

def ReadKddsToBeCalculated(fname):
    """
    self explanatory
    """

    listKdds=[]

    with open(fname,'r') as f:
        for line in f:
            listKdds.append(line.rstrip('\n'))

    return listKdds

def cvt_kdd_to_gname(kdd):
    """
    given Kdd, convert the name into gcloud one
    """
    t = kdd
    t = t.lower()
    t = t. replace('_', '-')
    
    return t
    
def read_template(template):
    """
    read and return template file as JSON
    """
    data = None
    with open(template) as data_file:    
        data = json.load(data_file)

    return data    
    
def make_pod_from_template(temjson, kdd, docker2run):
    """
    given JSON from template and kdd, make in-memory pod json
    """

    gname = cvt_kdd_to_gname( kdd )

    temjson["metadata"]["name"] = gname
    
    temjson["spec"]["containers"][0]["name"] = gname
    
    temjson["spec"]["containers"][0]["image"] = docker2run

    temjson["spec"]["containers"][0]["args"][0] = kdd

    return temjson
    
def make_json_pod(template, kdd, docker2run):
    """
    from template and Kdd to calc, make appropriate 
    """
    
    temjson = read_template(template)
    outjson = make_pod_from_template(temjson, kdd, docker2run)
    
    fname = "pod" + "_" + kdd + ".json"
    with open(fname, "w+") as f:
        f.write(json.dumps(outjson, indent=4))
        
    return fname
    
def read_config():
    """
    """
    with open("config_cluster.json") as data_file:    
        data = json.load(data_file)
    return data

def main(kdds_fname):
    """
    This method use existing cluster, and then
    for a given cluster launches pods (one pod per kdd),
    which are read from input file
    """

    cfg = read_config()

    CID   = cfg["CID"]
    ZID   = cfg["ZID"]
    mtype = cfg["machine-type"]
    
    docker  = cfg["docker"]
    gcr     = cfg["gcr"]
    project = cfg["project"]
    
    print("From config_cluster.json:")
    print(CID,ZID,mtype,docker,gcr,project)
    
    print("Reading KDDs list from {0}".format(kdds_fname))

    Kdds = ReadKddsToBeCalculated(kdds_fname)

    print("To compute KDDs: {0}".format(len(Kdds)))
    
    docker2run = os.path.join(gcr, project, docker) # full path to docker
    
    for kdd in Kdds:
        pod_name = make_json_pod("tempod.json", kdd, docker2run)
        cmd = "kubectl create -f " + pod_name
        rc = 0
        for k in range(0, 12): # several attempts to make a pod
            rc = subprocess.call(cmd, shell=True)
            if rc == 0:
                time.sleep(0.5)
                break

        if rc != 0:
            print("Cannot make kdd {0}".format(kdd))
            sys.exit(1)

if __name__ =='__main__':
    nof_args = len(sys.argv)

    if nof_args == 1:
        print("Use: addCluster list_of_KDDs")
        sys.exit(1)

    kdds_fname = ""
    if nof_args >= 2:
        kdds_fname = sys.argv[1]

    main(kdds_fname)

    sys.exit(0)

