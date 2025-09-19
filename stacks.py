# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 11:29:02 2024

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
    import pandas as pd
    from scipy.interpolate import interp1d
    

except ModuleNotFoundError as imp_error:
    print("Import Error: {0}\n".format(imp_error))
    print("Install the missing modules using: pip install modulename")
    
# =============================================================================
# Your code start here
# =============================================================================
# Get all the nk values
nk_folder = "nk_values/"

# Import the nk data from the folder nk_values
def import_nk(folder):
    """
    Import the nk data from the folder selected folder.

    Parameters
    ----------
    folder : string
        Folder containing the different files with the nk_values of each material.

    Returns
    -------
    Pandas dataframe with all the different materials in the folder

    """
    nk_db = {}
    for file in os.listdir(folder):
        # print(file)
        try:
            data = np.loadtxt(os.path.join(folder, file))
            # The wavelenght is in nm
            if data[0,0]>100:
                data_interpld = interp1d(data[:,0],data[:,1]+1j*data[:,2], fill_value="extrapolate")
            # the wavelenght is in micrometers
            else:
                data_interpld = interp1d(data[:,0]*1e3,data[:,1]+1j*data[:,2], fill_value="extrapolate")
            nk_db.update({file.split(".")[0]:data_interpld})
        except:
            pass
    nk_db = pd.Series(nk_db)
    return nk_db


def parse_external_stack(file):
    """
    Parse an external file to create a Stack Class object.

    Parameters
    ----------
    file : str.
        File with the information about a particular solar cell stack.

    Returns
    -------
    result : Stack Class
        A Stack Class object to perform further simulations.

    """
    stack_folder = "stacks/"
    # Initialize data holders
    thickness_list = {}
    nk_string_list = []
    nk_list = []
    parameters = {}
    name = file.rsplit(".", 1)[0]
    
    with open(os.path.join(stack_folder, file)) as file:
        contents = [line.replace("\n", "") for line in file.readlines()]
    if "Parameters" in contents:
        indices = [contents.index("Description"), contents.index("Stack"), contents.index("Parameters")]
        # Get the description
        description = contents[indices[0]+1:indices[1]-1][0]
        # Get the list of layers and their thicknesses
        stack = contents[indices[1]+1:indices[2]-1]
        for element in stack:
            data = element.split("\t")
            try:
                thickness_list[data[0]] = float(data[1])
            except ValueError:
                thickness_list[data[0]] = np.inf
            nk_string_list.append(data[2])
            nk_list = [nk_db.get(n) if n != "1" else lambda x:1 for n in nk_string_list]
        # Get the solar cell parameters
        params = contents[indices[2]+1:]
        for value in params:
            data = value.split("=")
            parameters[data[0]] = float(data[1])
        result = Stack(name, description, thickness_list, nk_list, parameters)
    else:
        indices = [contents.index("Description"), contents.index("Stack")]
        # Get the description
        description = contents[indices[0]+1:indices[1]-1][0]
        # Get the list of layers and their thicknesses
        stack = contents[indices[1]+1:]
        for element in stack:
            data = element.split("\t")
            try:
                thickness_list[data[0]] = float(data[1])
            except ValueError:
                thickness_list[data[0]] = np.inf
            nk_string_list.append(data[2])
            nk_list = [nk_db.get(n) if n != "1" else lambda x:1 for n in nk_string_list]
        result = Stack(name, description, thickness_list, nk_list)
    return result
    



# Define a class to hold the layer stack definition
class Stack:
    """
    A class to represent a solar cell stack.
    
    Attributes
    ----------
    description: str
        Description of the stack
        
    Methods
    -------
    make_d_list(None)
        Creates a list of thicknesses in the stack
    
    """
    
    def __init__(self, name, description, material_dict, nk_list, params = {"Voc":0.8, "Jsc":20.0, "FF":0.6, "Eff": 9.6}):
        self.name = name
        self.description = description
        self.material_dict = material_dict
        self.name_list = self.make_name_list()
        self.d_list = self.make_d_list()
        self.inc_list = self.__make_coherence_list()
        self.n_Data = nk_list
        self.params = params
        self.__self_test()
        
    def __make_coherence_list(self):
        coherence = []
        for t in self.material_dict.values():
            if float(t) < 2e3: # values larger than 2 micrometers are incoherent
                coherence.append('c')
            else:
                coherence.append('i')
        return coherence
        
    def __self_test(self):
        t_len = len(self.material_dict)
        c_len = len(self.inc_list)
        nk_len = len(self.n_Data)
        if t_len == c_len == nk_len:
            pass
        else:
            print("The number of elements in thickness, coherence and nk values does not match")
            
    def make_d_list(self):
        """
        Return the list of thicknesses for the different layers.

        Returns
        -------
        List
            The list of the material thickness in the stack.

        """
        return list(self.material_dict.values())
    
    def make_name_list(self):
        """
        Return the list of names for the different layers.

        Returns
        -------
        List
            The list of names in the stack.

        """
        return list(self.material_dict.keys())


# Create the n,k values database
nk_db = import_nk(nk_folder)
        
# Test
# Create Stack objects explicitely
# SiO2_thin_AZO = Stack("Fitted to thin AZO", 
#                       {"air": np.inf,
#                        "glass": 1.1e6,
#                        "blend":100},
#                       [lambda x:1, nk_db.nk_glass, lambda x:1])


single_PVXplus = Stack("PVXplus_single",
                       "Test of single junction PVXplus",
                        {"air": np.inf,
                        "glass": 1.1e6,
                        "ITO": 185,
                        "ZnO": 30,
                        "PVXplus": 100,
                        "HTLX": 30,
                        "Ag": 100,
                        "air2": np.inf},
                        [lambda x:1, nk_db.nk_glass, nk_db.nk_ITO_185_nm, nk_db.nk_ZnO, nk_db.nk_pvxplus, nk_db.nk_htlx, nk_db.nk_Ag, lambda x:1])

# Import an external stack from a file
# GS_ISO_2x_PVXplus = parse_external_stack("GS_ISO_2x_PVXplus.txt")

# BTA3_PVXplus_tandem = parse_external_stack("BTA3_PVXplus_tandem.txt")

# BTA3_PCBM_tandem = parse_external_stack("BTA3_PCBM_tandem.txt")

# BTA3_ITIC_tandem = parse_external_stack("BTA3_ITIC_tandem.txt")

# BTA3_GSISO_tandem = parse_external_stack("BTA3_GSISO_tandem.txt")

# GSISO_D18Y6_tandem = parse_external_stack("GSISO_D18Y6_tandem.txt")

# GSISO_IO4Cl_tandem = parse_external_stack("GSISO_IO4Cl_tandem.txt")

# GSISO_D18Y6_tandem_Ershuai = parse_external_stack("GSISO_D18Y6_tandem_Ershuai.txt")

# GSISO_IEICO4F_tandem = parse_external_stack("GSISO_IEICO4F_tandem.txt")