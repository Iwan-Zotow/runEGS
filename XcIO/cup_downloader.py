# -*- coding: utf-8 -*-

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
        
        logging.info("Cup downloader constructed")
        
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
        Compute hash fuR8O2IM01_KddCurveC.txtnctions of the downloaded cups, to be
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
                
    @staticmethod
    def single_load(src):
        """
        Load single cup from server
        """
        cmd = "wget"
                
        return subprocess.call([cmd, "-r", "-nH", "-nd", src], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def load(self):
        """
        Load cups info from server
        """
        
        self._rc = 0
        
        # form the command line
        #addr = "http://" + self._user_id + ":" + self._user_pass + "@" + self._host_ip
        addr = "http://" + "0.0.0.0:8080"
        
        fname = self._file_prefix + "_" + "KddCurveA.txt"
        src = os.path.join( addr, self._host_dir, fname )
        rc = cup_downloader.single_load(src)
        
        if rc != 0:
            self._rc = rc
            return
            
        fname = self._file_prefix + "_" + "KddCurveB.txt"
        src = os.path.join( addr, self._host_dir, fname )
        rc = cup_downloader.single_load(src)
        
        if rc != 0:
            self._rc = rc
            return
            
        fname = self._file_prefix + "_" + "KddCurveC.txt"
        src = os.path.join( addr, self._host_dir, fname )
        rc = cup_downloader.single_load(src)
        
        self._rc = rc        
        
    def rc(self):
        """
        Returns return code of the downloud operation
        """
        
        return self._rc
