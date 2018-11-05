# Docker to run dose calc remotely
FROM ubuntu:baseline
MAINTAINER O.K. <oleg.krivosheev@xcision.com>

RUN apt-get install -y --no-install-recommends python-pip && \
    apt-get install -y --no-install-recommends python-setuptools && \
    apt-get autoremove; apt-get autoclean; apt-get clean

# copy HEN_HOUSE & egsnrc

RUN mkdir -p /home/beamuser/egsnrc_mp
COPY egsnrc_mp /home/beamuser/egsnrc_mp

RUN mkdir -p /home/beamuser/HEN_HOUSE
COPY HEN_HOUSE /home/beamuser/HEN_HOUSE

RUN mkdir -p /home/beamuser/runEGS
COPY runEGS /home/beamuser/runEGS

RUN mkdir -p /home/beamuser/CUPS
COPY CUPS /home/beamuser/CUPS

COPY C25.egsphsp1 /home/beamuser/runEGS/C25.egsphsp1

COPY C15.egsphsp1 /home/beamuser/runEGS/C15.egsphsp1

COPY magickey.json /home/beamuser/runEGS/magickey.json

COPY config_gs.json /home/beamuser/runEGS/config_gs.json

# python environment
ENV PYTHONPATH /home/beamuser/runEGS/XcDefinitions:/home/beamuser/runEGS/XcMath:/home/beamuser/runEGS/XcMCCore:/home/beamuser/runEGS/XcIO

# EGS environment
ENV EGS_HOME /home/beamuser/egsnrc_mp/
ENV LD_LIBRARY_PATH /home/beamuser/HEN_HOUSE/egs++/dso/linux64:$LD_LIBRARY_PATH
ENV PATH /home/beamuser/egsnrc_mp/bin/x86_64-unknown-linux-gnu:/home/beamuser/HEN_HOUSE/bin/x86_64-unknown-linux-gnu:$PATH
ENV HEN_HOUSE /home/beamuser/HEN_HOUSE/
ENV OMEGA_HOME /home/beamuser/HEN_HOUSE/omega
ENV EGS_CONFIG /home/beamuser/HEN_HOUSE/specs/x86_64-unknown-linux-gnu.conf
ENV XZ_OPT=-9e

# running the show

WORKDIR /home/beamuser/runEGS
CMD /home/beamuser/runEGS/main.py

#CMD["R8O2IM01C25"]
