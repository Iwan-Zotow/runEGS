import os
import fnmatch

import process_cup

def process_set(set_dir, out_dir, zshift):
    """
    """
    for cup_dir in os.listdir(set_dir):
        if fnmatch.fnmatch(cup_dir, "R8O*C??"):
        
            dname = os.path.join(set_dir, cup_dir)
            process_cup.process_cup(dname, out_dir, zshift)

if __name__ == "__main__":
    process_set("/home/sphinx/gcloud", "qqq", -140.0)
