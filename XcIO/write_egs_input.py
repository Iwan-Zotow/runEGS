# -*- coding: utf-8 -*-

import names_helper
        
def write_input(template, file_prefix, coll, shot):
    """
    Write out egs input file from template
    """
    
    lines = []
    with open(template, "rt") as f:
        lines = f.readlines()
        
    # alter title
    qname = names_helper.make_qualified_name(file_prefix, coll, shot)
        
    lines[0] = qname + ";" + "SPAD=18cm;SAD=36cm" + "                                             #!GUI1.0\n"
               
    # alter phase space file name
    lines[2] = qname + names_helper.EGSPHAN_EXT + "\n"
    
    lines[43] = str(coll) + names_helper.EGSPHSF_EXT + "\n"
    
    fname = names_helper.make_egsinput_name(file_prefix, coll, shot)
    with open(fname, "wt") as f:
        f.writelines(lines)
        
    return fname
