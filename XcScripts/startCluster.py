#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import shutil
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

def make_cluster(CID, mach_type, nof_machs, ZID):
    """
    Given machine type and # of machines, creates cluster
    
    Parameters
    ------------
    
    CID: string
        cluster id
        
    mach_type: string
        machine type
        
    nof_machs: integer
        number of machines
        
    ZID: string
        zone id
    """
    
    cmd = "gcloud alpha container clusters create {0} --machine-type {1} --zone={3} --num-nodes {2}".format(CID, mach_type, nof_machs, ZID)
    
    rc = subprocess.call(cmd, shell=True)
    return rc
    
def auth_cluster(CID, ZID):
    """
    given zone id and cluser id, make authentication
    """

    cmd = "gcloud beta container get-credentials --cluster={0} --zone={1}".format(CID, ZID)
    rc = subprocess.call(cmd, shell=True)
    return rc
    
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

def main():
    """
    This method creates 
    in each running a docker image
    each being run with a particular kdd shot
    """
    
    CID = "egs"
    ZID = "us-central1-f"
    mtype  = "n1-standard-1"
    
    docker  = "egs-rc-4002"
    gcr     = "us.gcr.io"
    project = "direct-disk-101619"
    
    numberOfGCL = 8
    fileOfDesiredKdd='kddToBeCalculated.txt'

    Kdds = ReadKddsToBeCalculated(fileOfDesiredKdd)

    print('This script will create cluster with (at most) {0} google instances'.format(numberOfGCL-1)) # one for cluster management

    rc = make_cluster(CID, mtype, numberOfGCL-1, ZID)
    if rc != 0:
        print("Cannot make cluster")
        sys.exit(1)
        
    rc = auth_cluster(CID, ZID)
    if rc != 0:
        print("Cannot make auth")
        sys.exit(1)
    
    docker2run = os.path.join(gcr, project, docker) # full path to docker
    
    for kdd in Kdds:
        pod_name = make_json_pod("tempod.json", kdd, docker2run)
        cmd = "kubectl create -f " + pod_name
        rc = subprocess.call(cmd, shell=True)
        if rc != 0:
            print("Cannot make kdd {0}".format(kdd))
            sys.exit(1)

if __name__ =='__main__':
    main()

    sys.exit(0)

