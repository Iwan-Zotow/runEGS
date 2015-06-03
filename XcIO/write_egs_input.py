# -*- coding: utf-8 -*-

def construct_egsinput_name(file_prefix, coll, shot):
    """
    Makes EGS input name
    """
    
    return file_prefix + str(coll) + "_" + "Y{0}Z{1}".format(shot) + ".egsinp"
    

def write_input(template, file_prefix, coll, shot):
    """
    Write out egs input file from template
    """
    
    with open(template, "rt") as f:
        lines = f.readlines()
        
    # alter title
    lines[0] = file_prefix + str(coll) + ";" + "Y{0}Z{1}".format(shot) + \
               ";" + "SPAD=18cm;SAD=36cm" + "                #!GUI1.0"
               
    # alter phase space file name
    lines[2] = str(coll) + ".egsphsp1"
    
    lines[44] = str(coll) + ".egsphsp1"
    
    fname = construct_egsinput_name(file_prefix, coll, shot)
    with open(fname, "wt") as f:
        f.writelines(lines)
        
    return fname
