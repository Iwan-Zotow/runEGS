# Docker to run dose calc remotely
FROM ubuntu:15.04
MAINTAINER O.K. <oleg.krivosheev@xcision.com>

# commands and configuration
RUN apt-get update && \
    apt-get install -y python-numpy && \
    apt-get install -y net-tools && \
    apt-get install -y sshpass && \
    apt-get install -y iputils-ping && \
    apt-get install -y bzip2 && \
    apt-get autoremove; apt-get clean; apt-get autoclean

# copy HEN_HOUSE & egsnrc

RUN mkdir -p /root/egsnrc_mp
COPY egsnrc_mp /root/egsnrc_mp

RUN mkdir -p /root/HEN_HOUSE
COPY HEN_HOUSE /root/HEN_HOUSE

RUN mkdir -p /root/runEGS
COPY runEGS /root/runEGS

COPY C25.egsphsp1 /root/runEGS/C25.egsphsp1

RUN mkdir -p /root/.ssh
COPY known_hosts /root/.ssh/known_hosts

# python environment
ENV PYTHONPATH /root/runEGS/XcDefinitions:/root/runEGS/XcMath:/root/runEGS/XcMCCore:/root/runEGS/XcIO

# EHS environment
ENV EGS_HOME /root/egsnrc_mp/
ENV LD_LIBRARY_PATH /root/HEN_HOUSE/egs++/dso/linux64:$LD_LIBRARY_PATH
ENV PATH /root/egsnrc_mp/bin/x86_64-unknown-linux-gnu:/root/HEN_HOUSE/bin/x86_64-unknown-linux-gnu:$PATH
ENV HEN_HOUSE /root/HEN_HOUSE/
ENV OMEGA_HOME /root/HEN_HOUSE/omega
ENV EGS_CONFIG /root/HEN_HOUSE/specs/x86_64-unknown-linux-gnu.conf

# running the show

WORKDIR /root/runEGS
CMD /root/runEGS/main.py

#CMD["R8O2IM01C25"]
