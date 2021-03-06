# -*- coding: utf-8 -*-

import os
import shutil
import hashlib
import subprocess
import logging
import paramiko

import names_helper

class data_uploader(object):
    """
    Computed Data uploader
    """

    def __init__(self, wrk_dir, host_ip, host_port, host_dir, full_prefix, user_id, user_pass):
        """
        Constructor
        """

        logging.info("Start data uploader construction")
        logging.debug(wrk_dir)
        logging.debug(host_ip)
        logging.debug(host_port)
        logging.debug(host_dir)
        logging.debug(full_prefix)
        logging.debug(user_id)
        logging.debug(user_pass)

        self._wrk_dir = wrk_dir

        self._host_ip   = host_ip
        self._host_port = host_port
        self._host_dir  = host_dir

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

    def sign(self, cl):
        """
        Compute hash functions of the downloaded cups, to be
        used as a signature
        """

        logging.info("Start data signing")

        algo = "sha1"

        if not (algo in hashlib.algorithms):
            raise Exception("data_uploader", "No SHA1 hash available")

        self._hash = []

        # everything in work.dir: input, phantom, cups, etc
        for root, dirs, files in os.walk(self._wrk_dir):
            for f in files:

                hasher = hashlib.sha1()

                ctx = os.path.join(root, f)
                with open(ctx, "rb") as afile:
                    buf = afile.read()
                    hasher.update(buf)

                    self._hash.append((ctx, hasher.hexdigest()))

        # add phase space file signature
        phsf  = str(cl) + names_helper.EGSPHSF_EXT
        head,tail = os.path.split(self._wrk_dir)
        phsf = os.path.join(head, phsf)
        hasher = hashlib.sha1()
        with open(phsf, "rb") as afile:
            buf = afile.read()
            hasher.update(buf)

            self._hash.append((phsf, hasher.hexdigest()))

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

        dst = dir_name + ".tar.xz"
        rc = subprocess.call(["tar", "-cvJSf", dst, dir_name],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if rc != 0:
            logging.info("Error in data packing")
            logging.debug(rc)
            return (rc, None)

        logging.info("Done data packing")

        return (rc, dst)

    def upload_ssh(self, cl):
        """
        Upload data to the server using SSH protocol
        """

        logging.info("Start data uploading")

        cwd, dir_name = os.path.split(self._wrk_dir)

        self.sign(cl)
        rc, aname = self.compress_data(dir_name)

        if rc != 0:
            self._rc = rc
            return

        try:
            rc = subprocess.call(["sshpass", "-p", self._user_pass, "scp", aname, self._user_id +"@" + self._host_ip + ":" + "." ],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError:
            logging.debug("upload_ssh: OS failure")
            self._rc = rc
            return

        self._rc = rc

        logging.info("Done data uploading")

    def upload_ftp(self, cl):
        """
        Upload data to the server using FTP protocol
        """

        logging.info("Start data uploading")

        cwd, dir_name = os.path.split(self._wrk_dir)

        self.sign(cl)
        rc, aname = self.compress_data(dir_name)

        if rc != 0:
            self._rc = rc
            return

        try:
            dest = "ftp://" + self._user_id + ":" + self._user_pass + "@" + self._host_ip + "/" + self._host_dir + "/" + self._full_prefix[0:11] + "/"
            cmd = ["wput", aname, dest]
            rc  = subprocess.call(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError:
            logging.debug("upload_ftp: OS failure")
            #rc = -1
            self._rc = rc
            return

        self._rc = rc

        logging.info("Done data uploading")

    def upload_sftp(self, cl):
        """
        Upload data to the server using SFTP
        """

        logging.info("Start data uploading [SFTP]")

        cwd, dir_name = os.path.split(self._wrk_dir)
        self.sign(cl)
        rc, aname = self.compress_data(dir_name)

        if rc != 0:
            self._rc = rc
            return

        try:
            host = self._host_ip
            port = self._host_port
            transport = paramiko.Transport((host, port))

            username = self._user_id
            password = self._user_pass
            transport.connect(username=username, password=password)

            sftp = paramiko.SFTPClient.from_transport(transport)

            dest_dir = dir_name[0:dir_name.find("_")]
            remote_dir = os.path.join(self._host_dir, dest_dir)
            try:
                sftp.chdir(remote_dir)  # test if remote_dir exists
            except IOError:
                sftp.mkdir(remote_dir)
                sftp.chdir(remote_dir)

            destinationPath = os.path.join(remote_dir, aname)
            logging.info("Copying {0} to {1}".format(aname, destinationPath))
            sftp.put(aname, destinationPath)

            sftp.close()
            transport.close()

            rc = 0
        except OSError:
            logging.debug("upload_sftp: OS failure ")
            rc = -1
            self._rc = rc
            return

        self._rc = rc
        logging.info("Done with upload")


    def upload(self, cl):
        """
        Upload data to the server
        """

        return self.upload_sftp(cl)
        #return self.upload_ssh(cl)

    def rc(self):
        """
        Returns return code of the upload operation
        """

        return self._rc
