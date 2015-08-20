import os
import fnmatch

import process_cup

def process_set(set_dir, out_dir, zshift):
    """
    """
    
    tag = "R8O1IS"
    
    for k in range(1,10):
        cup_tag = tag + "0" + str(k)
        process_cup.process_cup(set_dir, cup_tag, out_dir, zshift)        

    tag = "R8O2IM"
    
    for k in range(1,10):
        cup_tag = tag + "0" + str(k)
        process_cup.process_cup(set_dir, cup_tag, out_dir, zshift)
            
    tag = "R8O2IM"
    
    for k in range(1,10):
        cup_tag = tag + "0" + str(k)
            process_cup.process_cup(set_dir, cup_tag, out_dir, zshift)

if __name__ == "__main__":
    process_set("/home/sphinx/gcloud", "qqq", 140.0)
