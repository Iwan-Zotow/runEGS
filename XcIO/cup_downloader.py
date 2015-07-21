# -*- coding: utf-8 -*-

import os
import shutil
import hashlib
import subprocess
import logging

class cup_downloader(object):
    """
    Downloads and holds cups        logging.info("Start data uploader construction")
        logging.debug(wrk_dir)
        logging.debug(host_ip)
 data
    """
    
    def __init__(self, host_ip, host_dir, cup_dir, file_prefix, user_id, user_pass):
        """
        Constructor
        """
        
        logging.info("Start cup downloader construction")
        logging.debug(host_ip)
        logging.debug(host_dir)
        logging.debug(cup_dir)
        logging.debug(file_prefix)
        logging.debug(user_id)
        logging.debug(user_pass)
        
        self._host_ip  = host_ip
        self._host_dir = host_dir
        self._cup_dir  = cup_dir
        
        self._file_prefix = file_prefix
        self._user_id     = user_id
        self._user_pass   = user_pass
        
        self._rc = 0
        
        logging.info("Done cup downloader construction")
        
    def single_load_ssh(self, src):
        """
        Load single cup using SSH protocol
        """
        try:
            logging.info("Start single cup download: {0}".format(src))
            
            rc = subprocess.call(["sshpass", "-p", self._user_pass, "scp", self._user_id +"@" + self._host_ip + ":" + src, self._cup_dir],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError:
            logging.debug("single_load_ssh: OS failure")
            rc = -1
            
        logging.info("One cup loaded")
            
        return rc
        
    def single_load_ftp(self, src):
        """
        Load single cup using FTP protocol
        """
        try:
            logging.info("Start single cup download: {0}".format(src))
            
            source = "ftp://" + self._user_id + ":" + self._user_pass + "@" + self._host_ip + "/" + src
            cmd = ["wget", "-r", "-nH", "-nd", "-P", self._cup_dir, source]
            rc = subprocess.call(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError:
            logging.debug("single_load_ftp: OS failure")
            rc = -1
            
        logging.info("One cup loaded")
            
        return rc
                
    def single_load(self, src):
        """
        Load single cup from server
        """
        return self.single_load_ftp(src)
        #return self.single_load_ssh(src)

    def load(self):
        """
        Load all cups info from server
        """
        
        logging.info("Start cup downloading")
        
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
        logging.info("Done cup downloading")        
        
    def rc(self):
        """
        Returns return code of the downloud operation
        """
        
        return self._rc
