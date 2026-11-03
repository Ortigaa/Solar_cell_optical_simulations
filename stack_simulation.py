# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 12:30:27 2024

@author: Rodrigo Delgado

Notes for PEP:
    Package and modules names: all lowercase, underscores when neccesary
    Functions: lowercase
    Class names: CapWords
    Variables: CapWords, preferred lowercase
    Exceptions: CapWords, with distinct prefix (e.g. ErrorWhatever)
    Constants: Uppercase
    
    

Todo
----

"""

# =============================================================================
# Import additional modules, if fail, raise an error
# =============================================================================
try:
    import numpy as np
    import matplotlib.pyplot as plt
    from tmm import tmm_core as tmm_core
    import pandas as pd
    import scipy.constants as c
    from scipy.interpolate import interp1d
    import itertools 
    import functions
    

except ModuleNotFoundError as imp_error:
    print("Import Error: {0}\n".format(imp_error))
    print("Install the missing modules using: pip install modulename")
    
# =============================================================================
# Your code start here
# =============================================================================

#Files

# Global definitions
EQE_folder = "EQE/"
outFolder = "output/"


class Simulation:
    """
    
    """
    
    def __init__(self, stack, light_source="AM15"):
        self.th = 0 # Incident angle
        self.polarization = 's' # Polarization of light
        self.lambda_step = 2 # wavelenght resolution
        self.lambda_list = np.arange(302, 1100, self.lambda_step) # Wavelenght scanned
        self.stack = stack
        self.light_source_name = light_source
        self.light_source = self.get_spectrum(light_source)(self.lambda_list) # Spectrum of light source in the desired wavelenght range
        self.name = stack.name
        
    def get_spectrum(self, light_source):
        """
        Generate the spectrum of the light source with correct units.

        Parameters
        ----------
        light_source : str
            Definition of the light source. For now can be "1sun" or "LowLight"

        Returns
        -------
        light_source : func
            Interpolation function of the original spectrum

        """
        if light_source == "AM15":
            # standard AM1.5 solar spectrum
            # You can find the original at rredc.nrel.gov/solar/spectra/am1.5
            spectrum = np.genfromtxt('sun_scout.csv', delimiter=',') # W/m2*nm
            
        if light_source == "LowLight":
            # Low light spectrum
            spectrum = np.genfromtxt('test_LED_warm_500lux.txt', delimiter='\t')
        
        # Convert units
        photon_spectrum = functions.convert_spectrum_np(spectrum) #p/m2*s*nm
        # Create a function to interpolate
        light_source = interp1d(photon_spectrum[:, 0], photon_spectrum[:, 1]*c.e*1e-1, bounds_error=False, fill_value="extrapolate") #number of photons*q
        return light_source
        
    def importEQE(self, filenames):
        """
        Import an EQE file.

        Parameters
        ----------
        filenames : TYPE
            DESCRIPTION.

        Returns
        -------
        interpolation_functions : TYPE
            DESCRIPTION.

        """
        # Probably the best is to:
        # - Import the measured data
        # - Create a fitting function that returns EQE(W) for every wavelenght
        interpolation_functions = []
        for file in filenames:
            data = np.genfromtxt(EQE_folder+file, skip_header=3, delimiter=",\t")
            data_interpolated = interp1d(data[:,0], data[:,1], fill_value="extrapolate")
            interpolation_functions.append(data_interpolated)
        return interpolation_functions
        
        
    def calculate_stack(self, absorber_layers, EQE_spectrum=[]):
        """
        Calculate the full optics and current of a given stack.

        Parameters
        ----------
        absorber_layers : List
            List with the names (strings) of the layers that the current is calculated for.
        
        EQE_spectum : List
            List of EQE filenames for the defined absorber_layers
            If empty EQE=1 will be used
            

        Returns
        -------
        None.
        Fill the results_single dictionary.
        results_single structure:
            - "Optics": Pandas dataframe:
                - Columns: wavelenght, Layer absorption (absorption in each layer of the stack),
                Stack_R (Total reflection of the stack), Stack_T (total transmission of the stack)
            - "Output": Pandas dataframe:
                - Columns: Thickness, Current density, with Indices the layer names
        """
        if len(EQE_spectrum)<1:
            self.EQE_spectrum = dict.fromkeys(absorber_layers, lambda x:1)
        else:
            interpolations = self.importEQE(EQE_spectrum)
            self.EQE_spectrum = dict(zip(absorber_layers, interpolations))
        
        optics = []
        output = {}
        self.results_single = {}
        for w in self.lambda_list:
            n_list = [n(w) for n in self.stack.n_Data]
            coh_tmm_data = tmm_core.inc_tmm(self.polarization, n_list, self.stack.d_list, self.stack.inc_list, self.th, w)
            layer_absorption = tmm_core.inc_absorp_in_each_layer(coh_tmm_data)
            stack_reflection = coh_tmm_data["R"]
            stack_transmission = coh_tmm_data["T"]
            optics.append([w, layer_absorption, stack_reflection, stack_transmission])
        for layer in absorber_layers:
            stack_index = self.stack.name_list.index(layer)
            absorp = [x[1][stack_index] for x in optics]
            current = sum(absorp*self.EQE_spectrum[layer](self.lambda_list)*self.light_source*self.lambda_step)
            output[layer] = self.stack.d_list[stack_index], current
        cols_results = ["Wavelenght","Layer Absorption", "Stack R", "Stack T"]
        result = pd.DataFrame(optics, columns=cols_results)
        out_pd = pd.DataFrame.from_dict(output, orient='index', columns=(["Thickness", "Current Density"]))
        self.results_single["Optics"] = result
        self.results_single["Output"] = out_pd
        
    def thickness_variation(self, absorber_layer_and_thickness, EQE_spectrum={}):
        """
        Calculate the stack optics for a given set of layer thicknesses variations.

        Parameters
        ----------
        absorber_layer_and_thickness : dict
            A dictionary containing the layer names as keys and a list of thicknesses as values
            ex.: {"BTA3": np.arange(80,160,10)}

        Returns
        -------
        None.
        Call the function "calculate_stack" for each combination and add the results to 
        "results_thickness"

        """
        variations = list(itertools.product(*absorber_layer_and_thickness.values()))
        print("The number of thicknesses combinations is {}".format(len(variations)))
        indices = []
        result = []
        for layer in absorber_layer_and_thickness.keys():
            indices.append(self.stack.name_list.index(layer))
        for value in variations:
            print("Variation : {0}={1}".format(list(absorber_layer_and_thickness.keys()),value))
            names = absorber_layer_and_thickness.keys()
            # print(names)
            for index ,t in zip(indices, value):
                self.stack.d_list[index] = t
            # print(self.stack.d_list)
            col_names = [*names] + ["Data"]
            self.calculate_stack(names, EQE_spectrum)
            result.append([*value, self.results_single])
        self.results_thickness = pd.DataFrame(data=result, columns=col_names)
        
    def print_stack(self):
        """
        Print the current stack being used.

        Returns
        -------
        None.

        """
        # Print the current stack being used
        names = self.stack.name_list
        thicknesses = self.stack.d_list
        print("Thicknesses in nm\n")
        print("Layer name\t Layer thickness")
        for n,t in zip(names, thicknesses):
            print("{0}\t {1}".format(n,t))
            
    def stack_absorption(self, layers={}):
        """
        Plot the absorption of each layer in the stack.

        Parameters
        ----------
        layers : dict, optional
            Dictionary containing the names (str, as keys) and thickness (int or float, as values).
            of layers in the stack that have some variation and need to be fixed. 
            If none is provided the last variation in the simulation is used. The default is {}.

        Returns
        -------
        None.

        """
        # Print the absorption of each layer in the stack
        # Either use the results_single or a selected entry in the results_thickness
        names = self.stack.name_list
        if len(layers) > 0:
            # Slice the results_thickness to the correct selection
            main_mask = True
            # Create a slicing mask base on the passed conditions
            for l, t in zip(layers.keys(), layers.values()):
                main_mask = main_mask & (self.results_thickness[l] == t)
            # Slice the dataframe to the correct row, then choose the "Data" cell, and the "Optics" dict
            data = self.results_thickness[main_mask]["Data"].iloc[0]["Optics"]
            wavelenght = np.array(data["Wavelenght"])
            all_abs = np.array(data["Layer Absorption"])
            # Put the data in the correct shape
            # An array where each row is the absorption of each layer
            all_abs = np.array([np.array(l) for l in all_abs]).T
            
            fig, ax = plt.subplots()
            for name, absorp in zip(names, all_abs):
                plt.plot(wavelenght, absorp, label=name)
            ax.set(xlabel='Wavelenght [nm]', ylabel='Absorption [a.u.]')
            ax.legend(loc='best', bbox_to_anchor=(1, 1))
            fig.tight_layout()
            
        else:
            # Use the results_single
            data = self.results_single["Optics"]
            wavelenght = np.array(data["Wavelenght"])
            all_abs = np.array(data["Layer Absorption"])
            # Put the data in the correct shape
            # An array where each row is the absorption of each layer
            all_abs = np.array([np.array(l) for l in all_abs]).T
            
            fig, ax = plt.subplots()
            for name, absorp in zip(names, all_abs):
                plt.plot(wavelenght, absorp, label=name)
            ax.set(xlabel='Wavelenght [nm]', ylabel='Absorption [a.u.]')
            ax.legend(loc='best', bbox_to_anchor=(1, 1))
            fig.tight_layout()
            
    def plot_absorption(self, layers={}, export=False):
        """
        Plot the absorption of selected layers.
        
        Plot the absorption vs. wavelenght for a given thickness of layers that
        have been simulated.

        Parameters
        ----------
        layers : dict, optional
            Dictionary containing the names (str, as keys) and thickness (int or float, as values)
            of layers in the stack that we want to plot the absorption for. The default is {}.

        Returns
        -------
        None.

        """
        main_mask = True
        # Create a slicing mask base on the passed conditions
        for l, t in zip(layers.keys(), layers.values()):
            main_mask = main_mask & (self.results_thickness[l] == t)
        # Slice the dataframe to the correct row, then choose the "Data" cell, and the "Optics" dict
        data = self.results_thickness[main_mask]["Data"].iloc[0]["Optics"]
        # Get the indices of the selected layers in the main stack
        indices_in_stack = []
        for layer in layers.keys():
            indices_in_stack.append(self.stack.name_list.index(layer))
        # print(indices_in_stack)
        wavelenght = np.array(data["Wavelenght"])
        all_abs = np.array(data["Layer Absorption"])
        absorp = []
        for w in all_abs:
            absorp.append([w[x] for x in indices_in_stack])
        # Plot the results
        fig, ax = plt.subplots()
        for i, name in enumerate(list(layers.keys())):
            plt.plot(wavelenght, [value[i] for value in absorp], label=name)
        ax.set(xlabel='Wavelenght [nm]', ylabel='Absorption [a.u.]')
        ax.legend(loc='best')
        ax.set_title(str(layers))
        if export:
            outArray = wavelenght
            for i, name in enumerate(list(layers.keys())):
                outArray = np.vstack((outArray, np.array([value[i] for value in absorp])))
            outName = outFolder+self.name+"_"+self.light_source_name+"_layer_absorption.txt"
            outHeader = "Wavelenght [nm]"
            for name in list(layers.keys()):
                outHeader += "\t" + name + " Jsc [mA/cm2]"
            np.savetxt(outName, outArray.T, header = outHeader)
                
        
    def plot_current_map(self, fixed_layers={}, export=False):
        """
        Plot a 2D contour plot of the generated current density in the stack.
        
        This function creates a 2D plot with the thickness of two layers in the stack
        as x and y axis and the minumum current of both layers as color coding. For more
        than two layers, other layer's thickness must be fixed in "fixed_layers".

        Parameters
        ----------
        fixed_layers : dict, optional
            Dictionary containing the names (str, as keys) and thickness (int or float, as values).
            of layers in the stack. It is used to slice the dataframe when more than 2 
            active layers are simulated, and the rest must be fixed. The default is {}.

        Returns
        -------
        A 2D contour plot, with axis representing the thickness of two layers and
        the color encoding the maximum current.

        """
        # Minimum current from the active layers as a function of thickness of all layers
        active_layer_number = len(self.results_thickness.columns) - 1
        # Remove the data colum from the DataFrame to loop faster
        reduced_df = self.results_thickness.drop("Data", axis=1)
        axes_labels = list(reduced_df.columns)
        thickness_list = [] # list of arrays with each element representing the
                            # thickness variation in each layer
        # Get the thickness variation for each active layer
        for col in reduced_df.columns:
            thickness_list.append(np.array(reduced_df[col].unique()))

        # If there are 3 or more axis, the thicknes of some layer has to be fixed and we make a contour plot
        if active_layer_number >= 3:
            if len(fixed_layers) < 1:
                print("To plot the current map for {0} materials, {1} thicknesses must specified in fixed_layers.".format(active_layer_number, active_layer_number-2))
            else:
                currents = [] # list of list with size t1*t2
                # Get the current values
                layer = list(fixed_layers.keys())
                thick = list(fixed_layers.values())
                for t in thickness_list[0]:
                    # For each thickness in the first active layer, create a slice of the 
                    # dataframe, selecting only the rows where the fixed_layer is correct
                    main_mask = self.results_thickness[axes_labels[0]] == t
                    for l, t in zip(layer,thick):
                        main_mask = main_mask & (self.results_thickness[l] == t)
                    data = self.results_thickness[main_mask]
                    current_row = []
                    for index, row in data.iterrows():
                        # Iterate over the rows in the reduced dataframe and get the minimum
                        # current from the generation in each layer
                        current_row.append(min(row["Data"]["Output"]["Current Density"]))
                    currents.append(current_row)
            
                fig, ax = plt.subplots()
                # Current list has to be transposed, because the argument in colormesh must be t2*t1
                im = ax.pcolormesh(thickness_list[0], thickness_list[1], np.array(currents).T, shading="auto")
                fig.colorbar(im, label=r'Current density [mA/cm$^2$]')
                ax.set(xlabel='{} thickness [nm]'.format(axes_labels[0]), ylabel='{} thickness [nm]'.format(axes_labels[1]))
                ax.set_title(str(fixed_layers))
        
        
        # If there are 2 axis make contour plot    
        elif active_layer_number == 2:
            
            currents = [] # list of list with size t1*t2
            # Get the current values
            for t in thickness_list[0]:
                # For each thickness in the first active layer, create a slice of the 
                # dataframe
                data = self.results_thickness.loc[self.results_thickness[axes_labels[0]] == t]
                current_row = []
                for index, row in data.iterrows():
                    # Iterate over the rows in the reduced dataframe and get the minimum
                    # current from the generation in each layer
                    current_row.append(min(row["Data"]["Output"]["Current Density"]))
                currents.append(current_row)
            
            fig, ax = plt.subplots()
            # Current list has to be transposed, because the argument in colormesh must be t2*t1
            im = ax.pcolormesh(thickness_list[0], thickness_list[1], np.array(currents).T, shading="auto")
            fig.colorbar(im, label=r'Current density [mA/cm$^2$]')
            ax.set(xlabel='{} thickness [nm]'.format(axes_labels[0]), ylabel='{} thickness [nm]'.format(axes_labels[1]))
            if export:
                # Create dataFilename
                outName = outFolder+self.name+"_"+self.light_source_name+"_current_map.txt"
                # Stack the currents matrix with the first axis
                outData = np.vstack((np.array(thickness_list[1]), np.array(currents)))
                # Create a new axis with a leading zero, so it has the dimensions
                # of the new matrix data (outData)
                new_axis = np.array(thickness_list[0])
                new_axis = np.insert(new_axis,0,0)
                # Stack the new axis with the previous matrix
                outArray = np.vstack((new_axis, np.flipud(outData.T)))
                outHeader = "1st Row {} thickness [nm], 1st Column {} thickness [nm]".format(*axes_labels)
                np.savetxt(outName, outArray, header = outHeader)
        else:
            print("A contour plot can not be made with this number of axis")

    def plot_j_vs_t(self, current_layer, variation_layer, thickness_layer=0, fixed_layers={}):
        """
        Plot the resulting current of "layer_current" as a function of the thickness of "variation_layer".
        
        "current_layer" and "variation_layer" can be the same, in which case the thickness of
        other layers must be specify in "fixed_layers".
        If more than 2 layers are taken as absorber in the simulation, the rest of the layers thicknesses must be
        fixed.
        
        Parameters
        ----------
        current_layer : str
            The layer name of which the current wish to be calculated
        variation_layer : str
            The layer name from which the different thicknesses will be taken
        thickness_layer : Int or Float, optional
            A fixed value for the thickness of "current_layer". The default is 0.
        fixed_layers : dict, optional
            Dictionary for additional layers that have a fixed value for plotting.
            Keys: str. Names of the layers
            Values: int or float. Thickness value
        
        Returns
        -------
        A plot.

        """
        # Create a dataframe from the original
        # If "fixed_layers" are used, then slice the original with regards to
        # their fixed thickness values
        if len(fixed_layers) > 0:
            data = self.results_thickness
            for o, t in zip(list(fixed_layers.keys()), list(fixed_layers.values())):
                data = data.loc[self.results_thickness[o] == t]
        # else use the original dataframe without slicing
        else:
            data = self.results_thickness
        # If the thickness of the layer we want the current calculated is fixed
        if thickness_layer != 0:
            # Create a sliced dataframe with only the selected layer thickness
            subdf = data.loc[data[current_layer] == thickness_layer]
            # Get the thickness variation for the other layer
            thickness_var = np.array(subdf[variation_layer].unique())
            # Get the current density values for the current_layer
            current = np.array([subdf["Data"][j]["Output"]["Current Density"][current_layer] for j in list(subdf.index)])
            # Plot the results
            fig, ax = plt.subplots()
            ax.scatter(thickness_var, current, label="{0} = {1} nm".format(current_layer, thickness_layer))
            ax.set(xlabel='{} thickness [nm]'.format(variation_layer), ylabel=r'{} current density [mA/cm$^2$]'.format(current_layer))
        # If we want to plot the results for all the simulated thicknesses of the "current_layer"
        else:
            # Get a list of the layer1 thicknesses
            layer1_t_list = list(data[current_layer].unique())
            # Get a list of the layer2 thicknesses
            layer2_t_list = list(data[variation_layer].unique())
            sliced_data = []
            # Create slices of the dataframe for each t in layer1
            for t in layer1_t_list:
                sliced_data.append(data.loc[data[current_layer] == t])
            currents = [] # List of arrays
            # Get the current calculated for each thickness
            for subdf in sliced_data:
                current = np.array([subdf["Data"][j]["Output"]["Current Density"][current_layer] for j in list(subdf.index)])
                # if the current and the thickness variation are for the same layer
                # "current" will be a single value, so no need for arrays
                if len(current) == 1:
                    current = float(current)
                currents.append(current)
            # Plot the results
            fig, ax = plt.subplots()
            # If the current and the thickness variation are for the same layer
            if current_layer == variation_layer:
                ax.scatter(layer2_t_list, currents)
                ax.set_title(str(fixed_layers))
            # In other cases
            else:
                for i, t1 in enumerate(layer1_t_list):
                    ax.scatter(layer2_t_list, currents[i], label="{0}={1} nm".format(current_layer, t1))
            ax.legend(loc='best', bbox_to_anchor=(1, 0.5))
            ax.set(xlabel='{} thickness [nm]'.format(variation_layer), ylabel=r'{} current density [mA/cm$^2$]'.format(current_layer))
            ax.set_title(str(fixed_layers))
            fig.tight_layout()

    def find_max_current(self):
        """
        Find the combination with the maximum current from a thickness variation.
        
        For a variation in thickness on several layers, this function finds the
        maximum and prints it to the terminal. It also returns a dictionary that
        can be passed as argument to the "plot_absorption" function.

        Returns
        -------
        Dict
            A dictionary with layer names as keys and thickness as values for 
            the combination with higher current.

        """
        data = self.results_thickness
        self.summary = self.results_thickness.drop("Data", axis=1)
        min_currents = []
        for index, row in data.iterrows():
            min_currents.append(min(row["Data"]["Output"]["Current Density"]))
        self.summary["Current"] = min_currents
        
        max_row = self.summary[self.summary['Current']==self.summary['Current'].max()].to_dict(orient="records")
        print("\n")
        print("The maximum current is at:")
        print(max_row[0])
        max_row[0].pop("Current")
        # print(max_row[0])
        return max_row[0]
    
    def print_row(self, fixed_layers = {}):
        """
        Print the output of a selected row from the results_thickness dataframe.
        
        Use a dictionary of layers names and thicknesses to slice the results_thickness dataframe.
        This will return the current generated in each active layer.

        Parameters
        ----------
        fixed_layers : dict, optional
            Dictionary with layer names as keys and thickness values as values. The default is {}.

        Returns
        -------
        None.

        """
        main_mask = True
        for l, t in zip(fixed_layers.keys(), fixed_layers.values()):
            main_mask = main_mask & (self.results_thickness[l] == t)
        data = self.results_thickness[main_mask]["Data"].iloc[0]["Output"]
        print(data)
        