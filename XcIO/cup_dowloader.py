# -*- coding: utf-8 -*-
"""
Created on Wed May 06 16:46:37 2015

@author: Oleg.Krivosheev
"""

import os
import shutil
import hashlib
import subprocess
import logging

class cup_downloader:
    """
    Downloads and holds cups data
    """
    
    def __init__(self, host_ip, host_dir, cup_dir, file_prefix, user_id, user_pass):
        """
        Constructor
        """
        self._host_ip  = host_ip
        self._host_dir = host_dir
        self._cup_dir  = cup_dir
        
        self._file_prefix = file_prefix
        self._user_id     = user_id
        self._user_pass   = user_pass
    
        self._rc = 0
        
        logging.info()
        
    def clean(self):
        """
        Clear output directory
        """
        for root, dirs, files in os.walk(self._cup_dir):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
                
        self._rc = 0
        
    def sign(self):
        """
        Compute hash functions of the downloaded cups, to be
        used as a signature
        """
        if not hashlib.algorithms.contains("sha1"):
            raise Exception("cup_downloader", "No SHA1 hash available")
            
        hasher = hashlib.sha1();
        self._hash = []
        for root, dirs, files in os.walk(self._cup_dir):
            for f in files:
                ctx = os.path.join(root, f)
                val = hasher.update(ctx)
                self._hash.append(val)

    def load(self):
        """
        Load cup info from server
        """
        # form the command line
        cmd = "wget"
                
        src = "ftp://" + self._user_id + ":" + self._user_pass + "@" + self._host_ip
        files = self._file_prefix + "*" + ".txt"
        src = os.path.join( src, self._host_dir, self._host_d, files )
        rc = subprocess.call([cmd, "-r", "-nH", "-nd", src], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        self._rc = rc        
        
    def rc(self):
        """
        Returns return code of the downlowd operation
        """
        
        return self._rc
