#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on: Jul 27 2015

Created by: Florin Neacsu

Last modified: Jul 27 2015, 21:34:22

Copyright Xcision LLC.
"""


import subprocess
import os
import shutil
import shlex


def main():
    """
    This method will close any gcloud instances that does not have a docker running
    The gcloud instances are selected from those haveing a name matching a pattern
    """

    gclName='egs'
    zone='us-central1-a'
    dockerImage='egs-single-shot'
    dockerImageLocation='us.gcr.io/direct-disk-101619/'


    #Let's get all the running instances
    cmdListImages = 'gcloud compute instances list'
    rc = subprocess.Popen([cmdListImages], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = rc.stdout.read()
    
    # output contains at least one line which is the header and we can ignore
    # if there are more lines, those contain details on the running instances

    #lets parse this output

    listOfInstances = output.split('\n')

    print output

    for i in range(1,len(listOfInstances)-1):
        # each line contains info such as name, zone, machine-type etc 
        # ...see output of `gcloud compute instances` list for ecample
        # we split that by empty spaces
        # then remove the entries containing just blanks with `filter`
        # hence we obtain a list with the separated information
        # we will need the external IP for ssh

        infoAboutInstance = filter(None,listOfInstances[i].split(' '))
        print infoAboutInstance[4]
        cmdDocker = "ssh -i ~/.ssh/id_rsa -o UserKnownHostsFile=/dev/null -o CheckHostIp=no -o StrictHostKeyChecking=no beamuser@{0} sudo docker ps".format(infoAboutInstance[4])
        args = shlex.split(cmdDocker)
        #print args
        rc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #output = rc.stdout.read()
        output, err = rc.communicate()
        listOfDockers = output# output.split('\n')
        
        #print listOfDockers
        runningDocker=0

        if (len(listOfDockers)>1):
            for i in range(0,len(listOfDockers)-1):
                #print 'Line {0} is {1}'.format(i,listOfDockers[i])
                if dockerImage in listOfDockers[i]:
                    runningDocker+=1
            #print listOfDockers[1]
            t=1
        if (runningDocker<1):
            print '\tThis instance is not doing anything...'
            print '\tShutting it down...'
            cmdShutdown="gcloud compute instances delete --zone {0} {1}".format(zone,infoAboutInstance[0])
            print cmdShutdown
            args = shlex.split(cmdShutdown)
            
            rc= subprocess.Popen(cmdShutdown, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            #output = rc.stdout.read()
            rc.stdin.write("y\n")
            #output, err = rc.communicate()
            #print output, err
        else:
            print 'There is stuff running... Let it run'
        

        #print output


if __name__ == '__main__':
    main()
