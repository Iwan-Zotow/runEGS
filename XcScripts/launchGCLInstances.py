#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os
import shutil


def ReadKddsToBeCalculated(fname):
    """
    self explanatory
    """

    listKdds=[]

    with open(fname,'r') as f:
        for line in f:
            listKdds.append(line.rstrip('\n'))

    return listKdds

def obtainInstanceInformation(instanceName):
    """
    Returns information of the instance under the format

    ['nameOfInstance','theZone','machineType,'internalIP','externalIP','status']
    
    """

    cmd="gcloud compute instances list {0} ".format(instanceName)
    rc=subprocess.Popen([cmd],shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = rc.stdout.read()
    # output contains 2 line, so we split it by \n
    # the first one is the header so we ingnore it
    # we split the second 1 by empty spaces
    # then remove those empty spaces with filer
    infoAboutInstance = filter(None,output.split('\n')[1].split(' '))

    #infoAbout instances is something like ['nameOfInstance','theZone','machineType,'internalIP','externalIP','status']

    return infoAboutInstance

def obtainIP(instanceName):
    """
    Returns the external ip of the instance
    """
    info = obtainInstanceInformation(instanceName)
    
    #print info[4]
    return info[4]

def main():
    """
    This method creates a number of gcloud instances
    in each running a docker image
    each being run with a particular kdd shot
    """

    gclName='egs'
    zone='us-central1-a'
    imageType='container-vm'
    machineType='n1-standard-1'
    dockerImage='egs-single-shot'
    dockerImageLocation='us.gcr.io/direct-disk-101619/'
    numberOfGCL=8
    fileOfDesiredKdd='kddToBeCalculated.txt'

    listOfKdds = ReadKddsToBeCalculated(fileOfDesiredKdd)
    numOfKdds = len(listOfKdds)

    itMax = min(numOfKdds,numberOfGCL)

    print 'This script will create (at most) {0} google instances'.format(numberOfGCL)

    for i in range(0,itMax):
        gclInstance='{0}-{1}'.format(gclName,listOfKdds[i]).replace('_','-').lower()
        print 'Creating {0}'.format(gclInstance)
        cmd="gcloud compute instances create {0} --zone {1} --image {2} --machine-type {3}".format(
                gclInstance,
                zone,
                imageType,
                machineType)
        #print cmd
        rc=subprocess.call(cmd, shell=True)#, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    for i in range(0,itMax):
        gclInstance='{0}-{1}'.format(gclName,listOfKdds[i]).replace('_','-').lower()
        
        ipAddr = obtainIP(gclInstance)
        #print ipAddr
        cmdDocker="sudo docker pull {0}{1}; sudo docker run -d -t {0}{1} python main.py {2};".format(dockerImageLocation,dockerImage,listOfKdds[i])
        cmd="ssh -i ~/.ssh/id_rsa -o UserKnownHostsFile=/dev/null -o CheckHostIp=no -o StrictHostKeyChecking=no beamuser@{0} \'{1}\'".format(ipAddr,cmdDocker)
        print cmd
        rc=subprocess.call(cmd, shell=True)







if __name__ =='__main__':
    main()

