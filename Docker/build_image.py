#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

rc = subprocess.call(["mkdir", "-p", "runEGS"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
rc = subprocess.call(["cd", "runEGS"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
rc = subprocess.call(["svn", "checkout", "https://192.168.1.230/svn/XCSW/MC_simulation/MC_code/branches/oleg/PSrework/trunk", "."], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
rc = subprocess.call(["cd", ".."], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
rc = subprocess.call(["docker", "build", "-t", "ubuntu:dxyz",  "."], stderr=subprocess.PIPE)

