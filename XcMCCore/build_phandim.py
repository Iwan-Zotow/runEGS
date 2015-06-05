# -*- coding: utf-8 -*-

import numpy as np
import logging

import phandim

def invariant(shot, the_range, steps, nr):
        """
        Check phantom parameters
        
        Parameters
        ----------
        
        shot: float
            shot position, mm
        the_range: (float,float)
            phantom range, (min,max), mm
        steps: (float,float)
            steps to do in phantom, (small,large), mm
        nr: integer
            number of small steps, defined by collimator size
            
        returns: boolean
            True if ok, False otherwise
        """
        
        rmin, rmax = the_range
        
        smin, smax = steps
        
        if (np.isnan(shot)):
            return False

        if (np.isnan(rmin)):
            return False
            
        if (np.isnan(rmax)):
            return False
            
        if (rmax <= rmin):
            return False

        if (np.isnan(smin)):
            return False
            
        if (np.isnan(smax)):
            return False
            
        if (smin > smax):
            return False
            
        if (nr < 1):
            return False
            
        return True

def build_one_boundary(shot, the_range, steps, nr):
        """
        Build phantom one dimensionboundaries from shot position and min/max range
        
        Parameters
        ----------
        
        shot: float
            shot position, mm
        the_range: (float,float)
            phantom range, (min,max), mm
        steps: (float,float)
            steps to do in phantom, (small,large), mm
        nr: integer
            number of small steps, defined by collimator size
            
        returns: array
            phantom one dimension boundaries
        """
        
        if (not invariant(shot, the_range, steps, nr)):
            raise ValueError("build_one_boundary", "invariant failed")
            
        rmin, rmax = the_range
        
        smin, smax = steps        

        # we know shot position is within the range

        # going backward
        bs = []

        # first, with small steps
        pos = shot      
        for k in range(0, nr+1):
            pos = shot - float(k) * smin
            bs.append(pos)
            if (pos < rmin):
                break

        # now large steps, continue from previous position
        while True:
            pos = pos - smax
            bs.append(pos)            
            if (pos < rmin):
                break
            
        # revert the list
        bs.reverse()
        
        # going forward
        
        # first, with small steps
        for k in range(1, nr+1):
            pos = shot + float(k) * smin
            bs.append(pos)
            if (pos > rmax):
                break
                    
        # now large steps, continue from previous position
        while True:
            pos = pos + smax
            bs.append(pos)            
            if (pos > rmax):
                break
            
        return bs

def build_phandim(shot, x_range, y_range, z_range, steps, nr):
        """
        Build phantom dimensions from shot position and min/max ranges
        
        Parameters
        ----------
        
        shot: (float,float)
            shot Y,Z position, mm
        x_range: (float,float)
            phantom X range, (min,max), mm
        y_range: (float,float)
            phantom Y range, (min,max), mm
        z_range: (float,float)
            phantom Z range, (min,max), mm
        steps: (float,float)
            steps to do in phantom, (small,large), mm
        nr: integer
            number of small steps, defined by collimator size
            
        returns: phandim
            phantom dimensions object
        """

        logging.info("building phandim")
        logging.debug(str(shot))
        logging.debug(str(x_range))
        logging.debug(str(y_range))
        logging.debug(str(z_range))
        logging.debug(str(steps))
        logging.debug(str(nr))

        ys, zs = shot
    
        # X boundaries, shot position always at 0
        bx = build_one_boundary(0.0, x_range, steps, nr)
        by = build_one_boundary( ys, y_range, steps, nr)
        bz = build_one_boundary( zs, z_range, steps, nr)
        
        return phandim.phandim(bx, by, bz)
