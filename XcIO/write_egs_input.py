# -*- coding: utf-8 -*-

import os
import logging

import names_helper
        
def write_input(wrk_dir, template, full_prefix, cl):
    """
    Write EGS input file from template
    
    Parameters
    ----------

    wrk_dir: string
        working directory

    template: string
        tempalte file name
        
    full_prefix: string
        full name without extention        
    """
    
    logging.info("Start making EGS input")
    logging.debug(wrk_dir)
    logging.debug(template)
    logging.debug(full_prefix)
    logging.debug(str(cl))
    
    lines = []
    with open(template, "rt") as f:
        lines = f.readlines()        
        
    lines[0] = full_prefix + ";" + "SPAD=18cm;SAD=36cm" + "                                             #!GUI1.0\n"
               
    # alter phase space file name
    lines[2] = os.path.join(wrk_dir, full_prefix + names_helper.EGSPHAN_EXT + "\n")
    
    lines[43] = str(cl) + names_helper.EGSPHSF_EXT + "\n"
    
    fname = os.path.join(wrk_dir, names_helper.make_egsinput_name(full_prefix))
    with open(fname, "wt") as f:
        f.writelines(lines)
        
    logging.info("Done making EGS input")
    logging.debug(fname)
    
    return fname

