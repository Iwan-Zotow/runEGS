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
    Read list of KDDs from file to be calculated

    Parameters
    ------------

    fname: string
        file name of the KDDs list

    returns: list
        all KDDs from fname
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

    returns: integer
        return code from gcloud call
    """

    cmd = "gcloud container clusters create {0} --machine-type {1} --zone {3} --num-nodes {2}".format(CID, mach_type, nof_machs, ZID)

    rc = subprocess.call(cmd, shell=True)
    return rc

def auth_cluster(CID, ZID):
    """
    Given zone id and cluser id, make authentication

    Parameters
    ------------

    CID: string
        cluster ID

    ZID: string
        zone ID

    returns: integer
        return code from gcloud call
    """

    cmd = "gcloud container clusters get-credentials {0} --zone {1}".format(CID, ZID)
    rc = subprocess.call(cmd, shell=True)
    return rc

def cvt_kdd_to_gname(kdd):
    """
    Given Kdd, convert the name into gcloud compatible one
    Gcloud shall have small letters and dahs instead of underscore

    Parameters
    ------------

    kdd: string
        KDD name

    returns: string
        name suited for gcloud
    """

    t = kdd
    t = t.lower()
    t = t. replace('_', '-')

    return t

def read_template(template):
    """
    Read and return template file as JSON

    Parameters
    ------------

    kdd: string
        KDD name

    returns: dictionary
        JSON parsed as dictionary
    """
    data = None
    with open(template) as data_file:
        data = json.load(data_file)

    return data

def make_pod_from_template(temjson, kdd, docker2run):
    """
    Given JSON from template and kdd, make in-memory pod json

    Parameters
    ------------

    temjson: dictionary
        In-memory pod JSON

    kdd: string
        KDD to compute name

    docker2run: string
        docker image to run

    returns: dictionary
        modified JSON suitable for computation
    """

    gname = cvt_kdd_to_gname( kdd )

    temjson["metadata"]["name"] = gname

    temjson["spec"]["containers"][0]["name"] = gname

    temjson["spec"]["containers"][0]["image"] = docker2run

    temjson["spec"]["containers"][0]["args"][0] = kdd

    return temjson

def make_json_pod(template, kdd, docker2run):
    """
    From template and Kdd to calc, make appropriate pod JSON

    Parameters
    ------------

    template: string
        file name of the JSON template

    kdd: string
        KDD to compute name

    docker2run: string
        docker image to run

    returns: dictionary
        modified JSON suitable for computation
    """

    temjson = read_template(template)
    outjson = make_pod_from_template(temjson, kdd, docker2run)

    fname = "pod" + "_" + kdd + ".json"
    with open(fname, "w+") as f:
        f.write(json.dumps(outjson, indent=4))

    return fname

def read_config(cfname):
    """
    Read cluster configuration file as JSON

    Parameters
    ------------

    cfname: string
        cluster config name

    returns: dictionary
        JSON parsed as dictionary
    """
    with open(cfname) as data_file:
        data = json.load(data_file)
    return data

def main(kdds_fname, numberOfGCL):
    """
    This method creates a cluster, and then
    for a given cluster launches pods (one pod per kdd),
    which are read from input file

    Parameters
    ------------

    kdds_fname: string
        file name which contains list of KDDs to compute

    numberOfGCL: integer
        number of the nodes in the cluster
    """

    cfg = read_config("config_cluster.json")

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

    print("Making cluster with nodes: {0}".format(numberOfGCL))

    rc = make_cluster(CID, mtype, numberOfGCL, ZID)
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
        print("Use: startCluster list_of_KDDs <optional>number_of_nodes")
        print("Default machine is usually n1-highcpu-2 with 2CPUs, see config_cluster.json")
        print("Default # of nodes is 8")
        sys.exit(1)

    kdds_fname = ""
    if nof_args >= 2:
        kdds_fname = sys.argv[1]

    numberOfGCL = 8 # default number of nodes
    if nof_args > 2:
        numberOfGCL = int(sys.argv[2])

    main(kdds_fname, numberOfGCL)

    sys.exit(0)
