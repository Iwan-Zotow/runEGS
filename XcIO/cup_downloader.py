# -*- coding: utf-8 -*-

import os
import shutil
import hashlib
import subprocess
import logging

class cup_downloader(object):
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
                
    def single_load(self, src):
        """
        Load single cup from server
        """
        return subprocess.call(["sshpass", "-p", self._user_pass, "scp", self._user_id +"@" + self._host_ip + ":" + src, self._cup_dir],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def load(self):
        """
        Load all cups info from server
        """
        
        self._rc = 0
        
        # form the command line
        
        fname = self._file_prefix + "_" + "KddCurveA.txt"
        src = os.path.join( self._host_dir, fname )
        rc = self.single_load(src)
        
        if rc != 0:
            self._rc = rc
            return
            
        fname = self._file_prefix + "_" + "KddCurveB.txt"
        src = os.path.join( self._host_dir, fname )
        rc = self.single_load(src)
        
        if rc != 0:
            self._rc = rc
            return
            
        fname = self._file_prefix + "_" + "KddCurveC.txt"
        src = os.path.join( self._host_dir, fname )
        rc = self.single_load(src)
        
        self._rc = rc        
        
    def rc(self):
        """
        Returns return code of the downloud operation
        """
        
        return self._rc
