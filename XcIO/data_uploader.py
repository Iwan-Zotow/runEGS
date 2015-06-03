# -*- coding: utf-8 -*-
"""
Created on Mon Jun 01 15:32:43 2015

@author: Oleg.Krivosheev
"""

import os
import shutil
import hashlib
import subprocess

class data_uploader:
    """
    Computed Data uploader
    """

    def __init__(self, host_ip, host_dir, file_prefix, user_id, user_pass):
        """
        Constructor
        """
        self._host_ip  = host_ip
        self._host_dir = host_dir
        
        self._file_prefix = file_prefix
        self._user_id     = user_id
        self._user_pass   = user_pass
    
        self._rc = 0
        
    def clean(self):
        """
        Clear output directory
        """
        for root, dirs, files in os.walk(self._cup_dir):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        
    def sign(self):
        """
        Compute hash functions of the downloaded cups, to be
        used as a signature
        """
        if not hashlib.algorithms.contains("sha1"):
            raise Exception("data_uploader", "No SHA1 hash available")
            
        hasher = hashlib.sha1();
        self._hash = []
        for root, dirs, files in os.walk(self._cup_dir):
            for f in files:
                ctx = os.path.join(root, f)
                val = hasher.update(ctx)
                self._hash.append(val)

    def upload(self):
        """
        Load data to the server
        """
        # form the command line
        cmd = "wput"
                
        dest = "ftp://" + self._user_id + ":" + self._user_pass + "@" + self._host_ip
        files = self._file_prefix + "*" + ".3ddose"
        dest = os.path.join( dest, self._host_dir, self._host_d, self._file_prefix )

        rc = subprocess.call([cmd, files, dest], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        self._rc = rc

    def rc(self):
        """
        Returns return code of the downlowd operation
        """
        
        return self._rc
