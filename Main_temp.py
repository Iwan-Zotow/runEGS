# -*- coding: utf-8 -*-
"""
Created on Tue May 26 14:29:16 2015 by Florin.Neacsu

Copyright Xcision LLC.
"""


"""
For now, this is used for quick (integration) testing



"""

from XcDefinitions import XcConstants

from XcIO          import ReadICPparam
from XcIO          import ReadOCPparam
from XcIO          import ReadRDUparam

outputResult = ReadICPparam.ReadICPparam("D:\Python_tests\R8O2IM01.icpparam")

outputResult2 = ReadOCPparam.ReadOCPparam("D:\Python_tests\R8O3.ocpparam")

outputResult3 = ReadRDUparam.ReadRDUparam("D:\Python_tests\R8.rduparam")