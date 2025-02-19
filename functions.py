# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 12:06:45 2024

@author: Rodrigo Delgado

Notes for PEP:
    Package and modules names: all lowercase, underscores when neccesary
    Functions: lowercase
    Class names: CapWords
    Variables: CapWords, preferred lowercase
    Exceptions: CapWords, with distinct prefix (e.g. ErrorWhatever)
    Constants: Uppercase
    
    

TODO
----
"""

# =============================================================================
# Import additional modules, if fail, raise an error
# =============================================================================
try:
    import os
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy.constants as c
    

except ModuleNotFoundError as imp_error:
    print("Import Error: {0}\n".format(imp_error))
    print("Install the missing modules using: pip install modulename")
    
# =============================================================================
# Your code start here
# =============================================================================

def plot_spectrum(spectrum, convert=False, title='Spectrum Irradiance'):
    """
    Plot the AM1.5G spectrum.

    Parameters
    ----------
    spectrum : TYPE
        DESCRIPTION.
    convert : TYPE, optional
        DESCRIPTION. The default is False.
    title : TYPE, optional
        DESCRIPTION. The default is 'Spectrum Irradiance'.

    Returns
    -------
    photon_spectrum : TYPE
        DESCRIPTION.

    """
    fig, ax1 = plt.subplots()
    
    # Plot the original spectrum
    ax1.plot(spectrum[:, 0], spectrum[:, 1], color='blue')
    ax1.set_xlim([280, 1500])
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_xlabel('Wavelength [nm]')
    ax1.set_ylabel('Spectral Irradiance [Wm$^{-2}$nm$^{-1}$]', color='blue')
    ax1.set_title(title)
    
    if convert:
        # Convert and plot photon flux
        photon_spectrum = convert_spectrum_np(spectrum)
        ax2 = ax1.twinx()
        ax2.plot(photon_spectrum[:, 0], photon_spectrum[:, 1], color='orange')
        ax2.tick_params(axis='y', labelcolor='orange')
        ax2.set_ylabel('Photons [m$^{-2}$s$^{-1}$nm$^{-1}$]', color='orange')
    
    plt.show()

    if convert:
        # Calculate and print photon flux if conversion is done
        photon_flux = np.trapz(photon_spectrum[:, 1], photon_spectrum[:, 0])
        #print(f'Photon flux: {photon_flux * np.e * 1e-1} mA/cm^2/s')
    return photon_spectrum

def convert_spectrum_np(spectrum):
    """
    Spectrum input:
        y: Irradiance (W/m2/nm)
        x: Wavelength (nm)
    Converted otput:
        y: Number of photons (Np/m2/s/nm)
        x: Wavelength (nm)
    """
    converted = np.copy(spectrum)
    # Convert wavelength from nm to meters for energy calculation
    converted[:, 0] *= 1e-9  # wavelength to meters
    E = c.h * c.c / converted[:, 0]  # Energy in Joules
    converted[:, 1] /= (E )  # Convert irradiance to number of photons, adjusting for units
    converted[:, 0] /= 1e-9  # Convert wavelength back to nm for output
    return converted




    