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

# make home dir
RUN mkdir -p /home/kriol

# copy HEN_HOUSE & egsnrc

RUN mkdir -p /home/kriol/egsnrc_mp
COPY egsnrc_mp /home/kriol/egsnrc_mp

RUN mkdir -p /home/kriol/HEN_HOUSE
COPY HEN_HOUSE /home/kriol/HEN_HOUSE

RUN mkdir -p /home/kriol/runEGS
COPY runEGS /home/kriol/runEGS

COPY C25.egsphsp1 /home/kriol/runEGS/C25.egsphsp1

RUN mkdir -p /root/.ssh
COPY known_hosts /root/.ssh/known_hosts

# python environment
ENV PYTHONPATH /home/kriol/runEGS/XcDefinitions:/home/kriol/runEGS/XcMath:/home/kriol/runEGS/XcMCCore:/home/kriol/runEGS/XcIO

# EGS environment
ENV EGS_HOME /home/kriol/egsnrc_mp/
ENV LD_LIBRARY_PATH /home/kriol/HEN_HOUSE/egs++/dso/linux64:$LD_LIBRARY_PATH
ENV PATH /home/kriol/egsnrc_mp/bin/x86_64-unknown-linux-gnu:/home/kriol/HEN_HOUSE/bin/x86_64-unknown-linux-gnu:$PATH
ENV HEN_HOUSE /home/kriol/HEN_HOUSE/
ENV OMEGA_HOME /home/kriol/HEN_HOUSE/omega
ENV EGS_CONFIG /home/kriol/HEN_HOUSE/specs/x86_64-unknown-linux-gnu.conf

# running the show

WORKDIR /home/kriol/runEGS
CMD /home/kriol/runEGS/main.py

#CMD["R8O2IM01C25"]
