# -*- coding: utf-8 -*-
"""
Created on Wed May 06 21:23:51 2015

@author: Oleg.Krivosheev
"""

# holds index vs (name, density) tuple
class materials(object):
    """
    Class which holds dictionary of the materials,
    index vs tuple(name, density)
    """

    def __init__(self, fname):
        """
        Constructor
        
        Parameters
        ----------
        
        fname: string
            materials file name
        """
        self._mats = None
    
        lines = []
        with open(fname, "rt") as f:
            lines = f.readlines()

        if len(lines) == 0:
            raise RuntimeError("materials", "No lines were read from file")
                        
        self._mats = {}
        self._mats[0] = ("", -1.0) # material at zero index
        
        id = 1
        for line in lines:
            split = line.split(" ")
            split = [x for x in split if x] # remove empty lines
            t = (split[0], float(split[1]))
            self._mats[id] = t
            id += 1
    
    def __getitem__(self, idx):
        """
        Returns item given the index

        Parameters
        ----------
        
        idx: integer
            index of the material
        returns: (string,double) tuple
            material data
        """
        return self._mats[idx]

    def __len__(self):
        """
        Returns length of the material dictionary
        """
        return len(self._mats)

    def mats(self):
        """
        Returns material dictionary        
        """
        return self._mats

