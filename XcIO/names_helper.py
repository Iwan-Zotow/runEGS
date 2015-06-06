# -*- coding: utf-8 -*-

EGSPHAN_EXT = ".egsphant"
EGSINP_EXT  = ".egsinp"
EGSPHSF_EXT = ".egsphsp1"

def make_qualified_name(file_prefix, cl, shot):
    """
    Makes qualified name
    
    Parameters
    ----------
        
        file_prefix: string
            prefix with RU and cup info
        
        cl: collimator
            collimator info
    
        shot: (float,float) tuple
            shot position
        
    returns: string
        fully qualified cup name
    """
    return file_prefix + str(cl) + "_" + "Y{0}Z{1}".format(int(shot[0]),int(shot[1]))

def make_egsinput_name(file_prefix, cl, shot):
    """
    Makes EGS input name
    """
    
    return make_qualified_name(file_prefix, cl, shot) + EGSINP_EXT
