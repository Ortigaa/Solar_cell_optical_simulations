# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 08:48:59 2024

@author: Rodrigo Delgado

Notes for PEP:
    Package and modules names: all lowercase, underscores when neccesary
    Functions: lowercase
    Class names: CapWords
    Variables: CapWords, preferred lowercase
    Exceptions: CapWords, with distinct prefix (e.g. ErrorWhatever)
    Constants: Uppercase
    
    

TODO
"""

# =============================================================================
# Import additional modules, if fail, raise an error
# =============================================================================
try:
    import os
    import numpy as np
    import matplotlib.pyplot as plt
    

except ModuleNotFoundError as imp_error:
    print("Import Error: {0}\n".format(imp_error))
    print("Install the missing modules using: pip install modulename")
    
# =============================================================================
# Your code start here
# =============================================================================

# Change directory to the folder with the script and the data
dire = os.getcwd()

nk_data_dir = os.path.join(dire,"nk_values")
a_data_dir = os.path.join(dire,"absorption")
n_data_dir = os.path.join(dire,"refractive_index")
k_data_dir = os.path.join(dire,"attenuation_coefficient")


def separate_data(file):
    filename = os.path.basename(file)
    # print(filename)
    data = np.genfromtxt(file)
    wavelenght = data[:,0] # in nm
    n_list = data[:,1]
    k_list = data[:,2]
    a_list = (4*np.pi*k_list)/(wavelenght*1e-9) # in m-1
    name_absorption = "a_" + filename[3:]
    with open(os.path.join(a_data_dir, name_absorption), "w") as file:
        for w,a in zip(wavelenght, a_list):
            file.write(str(w) + "\t" + str(a) + "\n")
    name_refractive = "n_" + filename[3:]
    with open(os.path.join(n_data_dir, name_refractive), "w") as file:
        for w,n in zip(wavelenght, n_list):
            file.write(str(w) + "\t" + str(n) + "\n")
    name_k = "k_" + filename[3:]
    with open(os.path.join(k_data_dir, name_k), "w") as file:
        for w,k in zip(wavelenght, k_list):
            file.write(str(w) + "\t" + str(k) + "\n")
    


def get_nk_data(directory):
    filelist = os.listdir(directory)
    # print(filelist)
    for file in filelist:
        separate_data(os.path.join(directory,file))
        
        
get_nk_data(nk_data_dir)
    

