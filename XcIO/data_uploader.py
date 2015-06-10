# -*- coding: utf-8 -*-

import os
import shutil
import hashlib
import subprocess
import logging

class data_uploader(object):
    """
    Computed Data uploader
    """

    def __init__(self, wrk_dir, host_ip, host_dir, full_prefix, user_id, user_pass):
        """
        Constructor
        """
        
        logging.info("Start data uploader construction")
        logging.debug(wrk_dir)
        logging.debug(host_ip)
        logging.debug(host_dir)
        logging.debug(full_prefix)
        logging.debug(user_id)
        logging.debug(user_pass)
        
        self._wrk_dir = wrk_dir
        
        self._host_ip  = host_ip
        self._host_dir = host_dir
        
        self._full_prefix = full_prefix
        self._user_id     = user_id
        self._user_pass   = user_pass
    
        self._rc = 0
        
        logging.info("Done data uploader construction")
        
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
        
        logging.info("Start data signing")
        
        algo = "sha1"
        
        if not (algo in hashlib.algorithms):
            raise Exception("data_uploader", "No SHA1 hash available")
            
        self._hash = []
        
        for root, dirs, files in os.walk(self._wrk_dir):
            for f in files:

                hasher = hashlib.sha1()
                
                ctx = os.path.join(root, f)
                with open(ctx, "rb") as afile:
                    buf = afile.read()
                    hasher.update(buf)
                    
                    self._hash.append((ctx, hasher.hexdigest()))
                
        fname = os.path.join(self._wrk_dir, algo)
        with open(fname, "wt") as f:
            for l in self._hash:
                f.write(l[0])
                f.write(": ")
                f.write(l[1])
                f.write("\n")

        logging.info("Done data signing")
        
    def compress_data(self, dir_name):
        """
        Pack and compress everything outgoing
        
        Parameter
        ---------
        
        dir_name: string
            directory to pack and compress
        """
        
        logging.info("Start data packing")
        logging.debug(dir_name)
        
        dst = dir_name + ".tar.bz2"
        rc = subprocess.call(["tar", "-cvjSf", dst, dir_name],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                          
        if rc == 0:
            return (0, dst)
            
        logging.info("Done data packing")
        
        return (rc, None)

    def upload(self):
        """
        Upload data to the server
        """

        logging.info("Start data uploading")
        
        cwd, dir_name = os.path.split(self._wrk_dir)
        
        rc, aname = self.compress_data(dir_name)
        
        self.sign()
        
        rc = subprocess.call(["sshpass", "-p", self._user_pass, "scp", aname, self._user_id +"@" + self._host_ip + ":" + "." ],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)        
        
        self._rc = rc
        logging.info("Done data uploading")

    def rc(self):
        """
        Returns return code of the upload operation
        """
        
        return self._rc

