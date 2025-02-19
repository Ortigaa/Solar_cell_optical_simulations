# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 10:45:19 2024

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
    from numpy import inf, pi
    import matplotlib.pyplot as plt
    from tmm.tmm_core import (coh_tmm, unpolarized_RT, ellips,
                       position_resolved, find_in_structure_with_inf)
    import stacks
    

except ModuleNotFoundError as imp_error:
    print("Import Error: {0}\n".format(imp_error))
    print("Install the missing modules using: pip install modulename")
    
# =============================================================================
# Your code start here
# =============================================================================


def sample4():
    """
    Here is an example where we plot absorption and Poynting vector
    as a function of depth.
    """
    d_list = [inf, 100, 300, inf] #in nm
    n_list = [1, 2.2+0.2j, 3.3+0.3j, 1]
    th_0 = pi/4
    lam_vac = 400
    pol = 'p'
    coh_tmm_data = coh_tmm(pol, n_list, d_list, th_0, lam_vac)

    ds = np.linspace(-50, 400, num=1000) #position in structure
    poyn = []
    absor = []
    for d in ds:
        layer, d_in_layer = find_in_structure_with_inf(d_list, d)
        data = position_resolved(layer, d_in_layer, coh_tmm_data)
        poyn.append(data['poyn'])
        absor.append(data['absor'])
    # convert data to numpy arrays for easy scaling in the plot
    poyn = np.array(poyn)
    absor = np.array(absor)
    plt.figure()
    plt.plot(ds, poyn, 'blue', ds, 200*absor, 'purple')
    plt.xlabel('depth (nm)')
    plt.ylabel('AU')
    plt.title('Local absorption (purple), Poynting vector (blue)')
    
sample4()