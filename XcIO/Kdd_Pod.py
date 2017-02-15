# -*- coding: utf-8 -*-
from __future__ import print_function

# dicts with replacements
repl_pod2kdd = {"r":"R", "c":"C", "x":"X", "y":"Y", "z":"Z", "o":"O", "i":"I", "l":"L", "-":"_", "0":"0", "1":"1", "2":"2", "3":"3", "4":"4", "5":"5", "6":"6", "7":"7", "8":"8", "9":"9"}
repl_kdd2pod = {"R":"r", "C":"c", "X":"x", "Y":"y", "Z":"z", "O":"o", "I":"i", "L":"l", "_":"-", "0":"0", "1":"1", "2":"2", "3":"3", "4":"4", "5":"5", "6":"6", "7":"7", "8":"8", "9":"9"}

def pod2kdd(pod):
    """
    Given the pod in Kubernetes format, transform it into Kdd format
    """

    kdd = pod[:]
    kdd = kdd.upper()
    kdd = kdd.replace('-', '_')

    # kdd = "".join(map(lambda x: repl_pod2kdd[x], pod))
    return kdd

def kdd2pod(kdd):
    """
    Given the kdd shot format, transform it into Kubernetes format
    """
    
    pod = kdd[:]
    pod = pod.lower()
    pod = pod.replace('_', '-')

    # pod = "".join(map(lambda x: repl_kdd2pod[x], kdd))
    return pod

if __name__ == "__main__":
   
    print("r8o3il08c25-y20z65")
    print(pod2kdd("r8o3il08c25-y20z65"))
    print(kdd2pod("R8O3IL08C25_Y20Z65"))
    print(kdd2pod(pod2kdd("r8o3il08c25-y20z65")))
    print(pod2kdd(kdd2pod("R8O3IL08C25_Y20Z65")))

