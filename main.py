# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 12:12:43 2024

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
    import os
    import stacks
    from stack_simulation import Simulation
    

except ModuleNotFoundError as imp_error:
    print("Import Error: {0}\n".format(imp_error))
    print("Install the missing modules using: pip install modulename")
    
# =============================================================================
# Your code start here
# =============================================================================

# =============================================================================
# Usage Instructions
# =============================================================================
# - Make sure the 3 necessary modules are in the same folder:
#    functions.py, stacks.py, stack_simulation.py
# - Create the stack that you wish to simulate, either on the stack.py module, 
# or in an external text file (more instructions in the stacks.py module)
# - 

# Change directory to current script location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


#%% Test and instructions
# Create the simulation class from the stack, in this case a stack defined on 
# stacks.py
test = Simulation(stacks.single_PVXplus, light_source="LowLight")

# Perform a single calculation for the given stack
# On the simulation class the resulting optics and currents can be found
test.calculate_stack(["PVXplus"])
# Same simulation can be performed with known EQE values
# test.calculate_stack(["PVXplus"], EQE_spectrum=["EQE_PVXplus.txt"])

# The absorption of one layer can be plotted individually by indexing its name

# The whole stack absorption can be plotted
test.stack_absorption()

# Perform a thickness variations for the defined layers with EQE
# test.thickness_variation({"PVXplus":np.arange(50,100,5)}, EQE_spectrum=["EQE_PVXplus.txt"])
# Or without
test.thickness_variation({"PVXplus":np.arange(50,100,5)})

test.plot_j_vs_t("PVXplus", "PVXplus")

# More than one layer can be varied
# test.thickness_variation({"PVXplus":np.arange(50,100,10),
#                           "ZnO":np.arange(20,60,5)})

# Plot the absorption of one layer with the selected thickness
# Export the plot data to a txt file
test.plot_absorption(layers={"PVXplus":55}, export=True)

#%% Single PM6:GSISO in standard architecture for Ershuai

# Import from file
GSISO_single = stacks.parse_external_stack("GSISO_std_single.txt")
# Create simulation object
GSISO_single_sim = Simulation(GSISO_single)

# Calculate stack
GSISO_single_sim.calculate_stack(["GSISO"])
#Perform thickness variation
# GSISO_single_sim.thickness_variation({"GSISO":np.arange(80, 120, 10)})

# Plot absorption at the combination with maximum current
# GSISO_single_sim.plot_absorption(layers=GSISO_single_sim.find_max_current())
# Plot the absorption of each layer in the stack for a given GSISO thickness
# GSISO_single_sim.stack_absorption(layers={"GSISO":110})
GSISO_single_sim.stack_absorption()

#%% Single cell simulations

#%%%
BTA3_single = stacks.parse_external_stack("PBDBT_BTA3_single.txt")
BTA3_single_sim = Simulation(BTA3_single)
BTA3_single_sim.thickness_variation({"BTA3":np.arange(60, 70, 1.0)})
BTA3_single_sim.plot_j_vs_t("BTA3", "BTA3")
BTA3_single_sim.stack_absorption()
#%%%
PCBM_single = stacks.parse_external_stack("PM6_PCBM_single.txt")
PCBM_single_sim = Simulation(PCBM_single)
PCBM_single_sim.thickness_variation({"PCBM":np.arange(86, 94, 1.0)})
PCBM_single_sim.plot_j_vs_t("PCBM", "PCBM")
PCBM_single_sim.stack_absorption()
#%%%
ITIC_single = stacks.parse_external_stack("PM6_ITIC_single.txt")
ITIC_single_sim = Simulation(ITIC_single)
ITIC_single_sim.thickness_variation({"ITIC":np.arange(108, 115, 1.0)})
ITIC_single_sim.plot_j_vs_t("ITIC", "ITIC")
ITIC_single_sim.stack_absorption()
#%%%
GSISO_single = stacks.parse_external_stack("PM6_GSISO_single.txt")
GSISO_single_sim = Simulation(GSISO_single)
GSISO_single_sim.thickness_variation({"GSISO":np.arange(160, 170, 1.0)})
GSISO_single_sim.plot_j_vs_t("GSISO", "GSISO")
GSISO_single_sim.stack_absorption()
#%%%
PVXplus_single = stacks.parse_external_stack("PVXplus_single.txt")
PVXplus_single_sim = Simulation(PVXplus_single)
PVXplus_single_sim.thickness_variation({"PVXplus":np.arange(80, 85, 1.0)})
PVXplus_single_sim.plot_j_vs_t("PVXplus", "PVXplus")
PVXplus_single_sim.stack_absorption()
#%%%
D18Y6_single = stacks.parse_external_stack("D18_Y6_single.txt")
D18Y6_single_sim = Simulation(D18Y6_single)
D18Y6_single_sim.thickness_variation({"D18Y6":np.arange(40, 150, 10)})
D18Y6_single_sim.plot_j_vs_t("D18Y6", "D18Y6")
D18Y6_single_sim.stack_absorption()
#%%%
BTPec9_single = stacks.parse_external_stack("PM6_BTP-eC9-2Cl_single.txt")
BTPec9_single_sim = Simulation(BTPec9_single)
BTPec9_single_sim.thickness_variation({"BTPec9":np.arange(50, 60, 1.0)})
BTPec9_single_sim.plot_j_vs_t("BTPec9", "BTPec9")
BTPec9_single_sim.stack_absorption()
#%%%
IO4Cl_single = stacks.parse_external_stack("PM6_IO4Cl_single.txt")
IO4Cl_single_sim = Simulation(IO4Cl_single)
IO4Cl_single_sim.thickness_variation({"IO4Cl":np.arange(105, 115, 1.0)})
IO4Cl_single_sim.plot_j_vs_t("IO4Cl", "IO4Cl")
IO4Cl_single_sim.stack_absorption()

#%% Tandem cells

#%%% Tandem with PM6:PCBM and PVX plus subcells
# Create simulation object
PCBM_PVXplus_sim = Simulation(stacks.parse_external_stack("PCBM_PVXplus_tandem.txt"))

# Thickness variation of both active layers
PCBM_PVXplus_sim.thickness_variation({"PCBM":np.arange(60,160,10),
                                    "PVXplus":np.arange(40, 120, 10)})


# Plot the current map
PCBM_PVXplus_sim.plot_current_map(export=True)

# PLot absorption where the current is higher
PCBM_PVXplus_sim.plot_absorption(layers=PCBM_PVXplus_sim.find_max_current(), export=True)

#%%% Tandem with PBDB-T:BTA3 and PVX plus subcells
# Create simulation object
BTA3_PVXplus_sim = Simulation(stacks.BTA3_PVXplus_tandem)

# Thickness variation of both active layers
BTA3_PVXplus_sim.thickness_variation({"BTA3":np.arange(50,120,5),
                                    "PVXplus1":np.arange(50, 120, 5)})

# # With EQEs
# BTA3_PVXplus_sim.thickness_variation({"BTA3":np.arange(50,120,10),
#                                     "PVXplus1":np.arange(50, 120, 10)},
#                                       EQE_spectrum=["EQE_PBDBT-BTA3.txt", "EQE_PVXplus.txt"])

# Plot current of BTA3 layer as a function of PVXplus layer thickness for all
# the BTA3 layer thicknesses
BTA3_PVXplus_sim.plot_j_vs_t("BTA3", "PVXplus1", thickness_layer=110)

# Plot the current map
BTA3_PVXplus_sim.plot_current_map(export=True)

# PLot absorption where the current is higher
BTA3_PVXplus_sim.plot_absorption(layers=BTA3_PVXplus_sim.find_max_current(), export=True)

#%%% tandem with PBDB-T:BTA3 and PM6:PCBM
# Create simulation object
BTA3_PCBM_sim = Simulation(stacks.parse_external_stack("BTA3_PCBM_tandem.txt"))

# Thickness variation of both active layers
BTA3_PCBM_sim.thickness_variation({"BTA3":np.arange(50,120,5),
                                    "PCBM":np.arange(60, 130, 5)})

# Plot the current map
BTA3_PCBM_sim.plot_current_map(export=True)

# PLot absorption where the current is higher
BTA3_PCBM_sim.plot_absorption(layers=BTA3_PCBM_sim.find_max_current(), export=True)
#%%% tandem with PBDB-T:BTA3 and PM6:ITIC
# Create simulation object
BTA3_ITIC_sim = Simulation(stacks.parse_external_stack("BTA3_ITIC_tandem.txt"))

# Thickness variation of both active layers
BTA3_ITIC_sim.thickness_variation({"BTA3":np.arange(50,160,10),
                                    "ITIC":np.arange(50, 170, 10)})

# Plot the current map
BTA3_ITIC_sim.plot_current_map(export=True)

# PLot absorption where the current is higher
BTA3_ITIC_sim.plot_absorption(layers=BTA3_ITIC_sim.find_max_current(), export=True)
#%%% tandem with PBDB-T:BTA3 and PM6:GS-ISO
# Create simulation object
BTA3_GSISO_sim = Simulation(stacks.parse_external_stack("BTA3_GSISO_tandem.txt"))

# Thickness variation of both active layers
BTA3_GSISO_sim.thickness_variation({"BTA3":np.arange(50,160,10),
                                    "GSISO":np.arange(80, 210, 10)})

# Plot the current map
BTA3_GSISO_sim.plot_current_map(export=True)

# PLot absorption where the current is higher
BTA3_GSISO_sim.plot_absorption(layers=BTA3_GSISO_sim.find_max_current(), export=True)

#%%% tandem with PBDBT:BTA3 and PM6:BTP-eC9

# Import from file
BTA3_BTP_tandem = stacks.parse_external_stack("BTA3_BTPec9_tandem.txt")
# Create simulation object
BTA3_BTP_sim = Simulation(BTA3_BTP_tandem)
#Perform thickness variation
BTA3_BTP_sim.thickness_variation({"BTA3":np.arange(50,120, 5),
                                    "BTPec9":np.arange(50, 120, 5)})

# Plot the current map
BTA3_BTP_sim.plot_current_map(export=True)

BTA3_BTP_sim.plot_absorption(layers=BTA3_BTP_sim.find_max_current(), export=True)

#%%% tandem with PBDBT:BTA3 and PCE10:COi8DFIC

# Import from file
BTA3_Coi8_tandem = stacks.parse_external_stack("BTA3_Coi8_tandem.txt")
# Create simulation object
BTA3_Coi8_sim = Simulation(BTA3_Coi8_tandem)
#Perform thickness variation
BTA3_Coi8_sim.thickness_variation({"BTA3":np.arange(50,120, 5),
                                    "Coi8DFIC":np.arange(50, 120, 5)})

# Plot the current map
BTA3_Coi8_sim.plot_current_map(export=True)

BTA3_Coi8_sim.plot_absorption(layers=BTA3_Coi8_sim.find_max_current(), export=True)

BTA3_Coi8_sim.print_row(BTA3_Coi8_sim.find_max_current())

#%%% tandem with PBDBT:BTA3 and PCE10:IEICO2F

# Import from file
BTA3_IEICO2F_tandem = stacks.parse_external_stack("BTA3_IEICO2F_tandem.txt")
# Create simulation object
BTA3_IEICO2F_sim = Simulation(BTA3_IEICO2F_tandem)
#Perform thickness variation
BTA3_IEICO2F_sim.thickness_variation({"BTA3":np.arange(50,120, 5),
                                    "IEICO2F":np.arange(50, 120, 5)})

# Plot the current map
BTA3_IEICO2F_sim.plot_current_map(export=True)

BTA3_IEICO2F_sim.plot_absorption(layers=BTA3_IEICO2F_sim.find_max_current(), export=True)

BTA3_IEICO2F_sim.print_row(BTA3_IEICO2F_sim.find_max_current())

#%%% tandem with PM6:GS-ISO and BTA3 (same as before but reversed layers)

# Import from file
GSISO_BTA3_tandem = stacks.parse_external_stack("GSISO_BTA3_tandem.txt")
# Create simulation object
GSISO_BTA3_sim = Simulation(GSISO_BTA3_tandem)
#Perform thickness variation
GSISO_BTA3_sim.thickness_variation({"GSISO":np.arange(80, 190, 10),
                                    "BTA3":np.arange(50, 120, 10)})

# Plot the current map
GSISO_BTA3_sim.plot_current_map(export=True)

# PLot absorption where the current is higher
GSISO_BTA3_sim.plot_absorption(layers=GSISO_BTA3_sim.find_max_current(), export=True)

#%%% tandem with PM6:GSISO and PVXplus

# Import from file
GSISO_PVXplus_tandem = stacks.parse_external_stack("GSISO_PVXplus_tandem.txt")
# Create simulation object
GSISO_PVXplus_sim = Simulation(GSISO_PVXplus_tandem)
#Perform thickness variation
GSISO_PVXplus_sim.thickness_variation({"GSISO":np.arange(80, 190, 10),
                                    "PVXplus":np.arange(50, 120, 10)})

# Plot the current map
GSISO_PVXplus_sim.plot_current_map(export=True)

# PLot absorption where the current is higher
GSISO_PVXplus_sim.plot_absorption(layers=GSISO_PVXplus_sim.find_max_current(), export=True)
#%%% tandem with PM6:GSISO and D18:Y6

# Import from file

# Create simulation object
GSISO_D18Y6_sim = Simulation(stacks.parse_external_stack("GSISO_D18Y6_tandem.txt"))
#Perform thickness variation
GSISO_D18Y6_sim.thickness_variation({"GSISO":np.arange(80, 190, 10),
                                    "D18Y6":np.arange(50, 120, 10)})

# Plot the current map
GSISO_D18Y6_sim.plot_current_map(export=True)

# PLot absorption where the current is higher
GSISO_D18Y6_sim.plot_absorption(layers=GSISO_D18Y6_sim.find_max_current(), export=True)
#%%% tandem with PM6:GSISO and PM6:PCBM

# Import from file
GSISO_PCBM_tandem = stacks.parse_external_stack("GSISO_PCBM_tandem.txt")
# Create simulation object
GSISO_PCBM_sim = Simulation(GSISO_PCBM_tandem)
#Perform thickness variation
GSISO_PCBM_sim.thickness_variation({"GSISO":np.arange(80, 190, 10),
                                    "PCBM":np.arange(60, 130, 10)})

# Plot the current map
GSISO_PCBM_sim.plot_current_map(export=True)

# PLot absorption where the current is higher
GSISO_PCBM_sim.plot_absorption(layers=GSISO_PCBM_sim.find_max_current(), export=True)
#%%% tandem with PM6:GSISO and PM6:IO4Cl

# Create simulation object
GSISO_IO4Cl_sim = Simulation(stacks.parse_external_stack("GSISO_IO4Cl_tandem.txt"))
#Perform thickness variation
GSISO_IO4Cl_sim.thickness_variation({"GSISO":np.arange(70, 190, 10),
                                    "IO4Cl":np.arange(70, 210, 10)})

# Plot the current map
GSISO_IO4Cl_sim.plot_current_map(export=True)

# PLot absorption where the current is higher
GSISO_IO4Cl_sim.plot_absorption(layers=GSISO_IO4Cl_sim.find_max_current(), export=True)
#%%% tandem with PM6:GSISO and PM6:BTP-eC9

# Import from file
GSISO_BTPec9_tandem = stacks.parse_external_stack("GSISO_BTPec9_tandem.txt")

# Create simulation object
GSISO_BTPec9_sim = Simulation(GSISO_BTPec9_tandem)
#Perform thickness variation
GSISO_BTPec9_sim.thickness_variation({"GSISO":np.arange(80, 190, 10),
                                    "BTPec9":np.arange(50, 120, 10)})

# Plot the current map
GSISO_BTPec9_sim.plot_current_map(export=True)

# PLot absorption where the current is higher
GSISO_BTPec9_sim.plot_absorption(layers=GSISO_BTPec9_sim.find_max_current(), export=True)
#%%% tandem with PM6:GSISO and PTB7-Th:Coi8DFIC

# Import from file
GSISO_Coi8_tandem = stacks.parse_external_stack("GSISO_Coi8DFIC_tandem.txt")

# Create simulation object
GSISO_Coi8_tandem_sim = Simulation(GSISO_Coi8_tandem)
#Perform thickness variation
GSISO_Coi8_tandem_sim.thickness_variation({"GSISO":np.arange(80, 160, 10),
                                    "Coi8DFIC":np.arange(50, 120, 10)})

# Plot the current map
GSISO_Coi8_tandem_sim.plot_current_map()

GSISO_Coi8_tandem_sim.plot_absorption(layers=GSISO_Coi8_tandem_sim.find_max_current())

#%%% tandem with PM6:GSISO and PTB7-Th:IEICO2F

# Import from file
GSISO_IEICO2F_tandem = stacks.parse_external_stack("GSISO_IEICO2F_tandem.txt")

# Create simulation object
GSISO_IEICO2F_sim = Simulation(GSISO_IEICO2F_tandem)
#Perform thickness variation
GSISO_IEICO2F_sim.thickness_variation({"GSISO":np.arange(80, 160, 10),
                                    "IEICO2F":np.arange(50, 120, 10)})

# Plot the current map
GSISO_IEICO2F_sim.plot_current_map()

GSISO_IEICO2F_sim.plot_absorption(layers=GSISO_IEICO2F_sim.find_max_current())

#%%% tandem with PM6:GSISO and PTB7-Th:IEICO4F

# Import from file
GSISO_IEICO4F_tandem = stacks.parse_external_stack("GSISO_IEICO4F_tandem.txt")

# Create simulation object
GSISO_IEICO4F_sim = Simulation(GSISO_IEICO4F_tandem)
#Perform thickness variation
GSISO_IEICO4F_sim.thickness_variation({"GSISO":np.arange(80, 160, 10),
                                    "IEICO4F":np.arange(50, 120, 10)})

# Plot the current map
GSISO_IEICO4F_sim.plot_current_map()

GSISO_IEICO4F_sim.plot_absorption(layers=GSISO_IEICO4F_sim.find_max_current())



#%%% tandem with PM6:IO4Cl and PM6:PCBM

# Import from file
IO4Cl_PCBM_tandem = stacks.parse_external_stack("IO4Cl_PCBM_tandem.txt")

# Create simulation object
IO4Cl_PCBM_sim = Simulation(IO4Cl_PCBM_tandem)
#Perform thickness variation
IO4Cl_PCBM_sim.thickness_variation({"IO4Cl":np.arange(70, 190, 10),
                                    "PCBM":np.arange(60, 130, 10)})

# Plot the current map
IO4Cl_PCBM_sim.plot_current_map(export=True)
IO4Cl_PCBM_sim.plot_absorption(layers=IO4Cl_PCBM_sim.find_max_current(), export=True)

#%%% tandem with PM6:IO4Cl and PM6:ITIC

# Import from file
IO4Cl_ITIC_tandem = stacks.parse_external_stack("IO4Cl_ITIC_tandem.txt")

# Create simulation object
IO4Cl_ITIC_sim = Simulation(IO4Cl_ITIC_tandem)
#Perform thickness variation
IO4Cl_ITIC_sim.thickness_variation({"IO4Cl":np.arange(70, 190, 10),
                                    "ITIC":np.arange(50, 170, 10)})

# Plot the current map
IO4Cl_ITIC_sim.plot_current_map(export=True)
# Plot absorption at the combination with maximum current
IO4Cl_ITIC_sim.plot_absorption(layers=IO4Cl_ITIC_sim.find_max_current(), export=True)

#%%% tandem with PM6:IO4Cl and PVXplus

# Import from file
IO4Cl_PVXplus_tandem = stacks.parse_external_stack("IO4Cl_PVXplus_tandem.txt")

# Create simulation object
IO4Cl_PVXplus_tandem_sim = Simulation(IO4Cl_PVXplus_tandem)
#Perform thickness variation
IO4Cl_PVXplus_tandem_sim.thickness_variation({"IO4Cl":np.arange(70, 190, 10),
                                    "PVXplus":np.arange(50, 120, 10)})

# Plot the current map
IO4Cl_PVXplus_tandem_sim.plot_current_map(export=True)
# Plot absorption at the combination with maximum current
IO4Cl_PVXplus_tandem_sim.plot_absorption(layers=IO4Cl_PVXplus_tandem_sim.find_max_current(), export=True)

#%%% tandem with 2 PVXplus subcells

# Import from file
PVXplus_tandem = stacks.parse_external_stack("PVXplus_homo_tandem.txt")

# Create simulation object
PVXplus_sim = Simulation(PVXplus_tandem)
#Perform thickness variation
PVXplus_sim.thickness_variation({"PVXplus1":np.arange(50, 120, 10),
                                    "PVXplus2":np.arange(50, 120, 10)})

# # PEDOT thickness variation, with the optimal PVX layer thickness fixed
# PVXplus_sim.thickness_variation({"HTLX1":np.arange(40, 50, 5),
#                                  "AI1":np.arange(40, 50, 5),
#                                  "HTLX2":np.arange(40, 50, 5)})

# Plot the current map
# PVXplus_sim.plot_current_map()
# Plot absorption at the combination with maximum current
PVXplus_sim.plot_absorption(layers=PVXplus_sim.find_max_current(), export=True)

PVXplus_sim.print_row(PVXplus_sim.find_max_current())

PVXplus_sim.print_row(fixed_layers={"PVXplus1":80, "PVXplus2":90})

#%%% tandem with PVXplus and D18:Y6

# Import from file
PVXplus_D18Y6_tandem = stacks.parse_external_stack("PVXplus_D18Y6_tandem.txt")

# Create simulation object
PVXplus_D18Y6_sim = Simulation(PVXplus_D18Y6_tandem)
#Perform thickness variation
PVXplus_D18Y6_sim.thickness_variation({"PVXplus":np.arange(50, 120, 10),
                                    "D18Y6":np.arange(50, 120, 10)})

# Plot the current map
PVXplus_D18Y6_sim.plot_current_map()
# Plot absorption at the combination with maximum current
PVXplus_D18Y6_sim.plot_absorption(layers=PVXplus_D18Y6_sim.find_max_current())

#%%% tandem with PTQ10:FCC-Cl and PM6:BTP-ec9

# Import from file
PTQ_BTP_tandem = stacks.parse_external_stack("PTQFCC_BTPec9_tandem.txt")
# Create simulation object
PTQ_BTP_sim = Simulation(PTQ_BTP_tandem)
#Perform thickness variation
PTQ_BTP_sim.thickness_variation({"PTQ":np.arange(50,200, 10),
                                    "BTPec9":np.arange(50, 120, 10)})

# Plot the current map
PTQ_BTP_sim.plot_current_map(export=True)

PTQ_BTP_sim.plot_absorption(layers=PTQ_BTP_sim.find_max_current(), export=True)

PTQ_BTP_sim.print_row(PTQ_BTP_sim.find_max_current())

#%%% tandem with PTQ10:FCC-Cl and PVXplus

# Import from file
PTQ_PVX_tandem = stacks.parse_external_stack("PTQFCC_PVXplus_tandem.txt")
# Create simulation object
PTQ_PVX_sim = Simulation(PTQ_PVX_tandem)
#Perform thickness variation
PTQ_PVX_sim.thickness_variation({"PTQ":np.arange(50,200, 10),
                                    "PVXplus":np.arange(50, 120, 10)})

# Plot the current map
PTQ_PVX_sim.plot_current_map(export=True)

PTQ_PVX_sim.plot_absorption(layers=PTQ_PVX_sim.find_max_current(), export=True)

PTQ_PVX_sim.print_row(PTQ_PVX_sim.find_max_current())

#%%% tandem with D18:FCC-Cl and PVXplus

# Import from file
D18_PVX_tandem = stacks.parse_external_stack("D18-FCC_PVXplus_tandem.txt")
# Create simulation object
# D18_PVX_sim = Simulation(D18_PVX_tandem)
# Low light simulation
D18_PVX_sim = Simulation(D18_PVX_tandem, light_source="LowLight")
#Perform thickness variation
D18_PVX_sim.thickness_variation({"D18FCC":np.arange(30,200, 10),
                                    "PVXplus":np.arange(50, 200, 10)})

# Plot the current map
D18_PVX_sim.plot_current_map(export=True)

D18_PVX_sim.plot_absorption(layers=D18_PVX_sim.find_max_current(), export=True)

D18_PVX_sim.print_row(D18_PVX_sim.find_max_current())

#%%% tandem with PM6:D18:L8-BO and PVXplus

# Import from file
ternary_PVX_tandem = stacks.parse_external_stack("PM6-D18-L8BO_PVXplus_tandem.txt")
# Create simulation object
# ternary_PVX_sim = Simulation(ternary_PVX_tandem)
ternary_PVX_sim = Simulation(ternary_PVX_tandem, light_source="LowLight")
#Perform thickness variation
ternary_PVX_sim.thickness_variation({"PM6D18":np.arange(30,200, 10),
                                    "PVXplus":np.arange(30, 200, 10)})

# Plot the current map
ternary_PVX_sim.plot_current_map(export=True)

ternary_PVX_sim.plot_absorption(layers=ternary_PVX_sim.find_max_current(), export=True)

ternary_PVX_sim.print_row(ternary_PVX_sim.find_max_current())
#%% Triple junction cell simulations

#%%% Triple cell with GS-ISO and 2 PVX-plus subcells

# Import from the stacks module
gs_iso_2pvxplus_sim = Simulation(stacks.GS_ISO_2x_PVXplus)

# Calculate the stack current for the 3 active layers
# gs_iso_2pvxplus_sim.calculate_stack(["PM6_GSISO", "PVXplus1", "PVXplus2"])

# Perform a thickness variation of the 3 layers
gs_iso_2pvxplus_sim.thickness_variation({"PM6_GSISO":np.arange(60,100,20),
                                          "PVXplus1":np.arange(60,100,20),
                                          "PVXplus2":np.arange(80, 120, 20)})

# Current as a function of layer thickness for first layer fixing the thickness
# of the other two layers
# gs_iso_2pvxplus_sim.plot_j_vs_t("PM6_GSISO", "PM6_GSISO", fixed_layers={"PVXplus1":60,"PVXplus2":80})

# Current of one layer as a function of other layer thickness, fixing the third layer thickness
# gs_iso_2pvxplus_sim.plot_j_vs_t("PM6_GSISO", "PVXplus1", fixed_layers={"PVXplus2":80})

# Current of one layer with different thicknesses as a function of the second layer thickness, fixing the thrid layer thickness
# gs_iso_2pvxplus_sim.plot_j_vs_t("PM6_GSISO", "PVXplus1", thickness_layer=60, fixed_layers={"PVXplus2":80})

# Thickness variation of only 2 layers
# gs_iso_2pvxplus_sim.thickness_variation({"PM6_GSISO":np.arange(60,100,10),
#                                             "PVXplus1":np.arange(60,100,10)})

# Plot the current map between GS_ISO and PVXplus1 for a fixed PVXplus2 layer thickness
# gs_iso_2pvxplus_sim.plot_current_map(fixed_layers={"PVXplus2":80})

# Plot the current of GS-ISO cell as a function of the thickness of PVXplus1
# gs_iso_2pvxplus_sim.plot_j_vs_t("PM6_GSISO", "PVXplus1")

# Plot the absoption of the selected layers
# gs_iso_2pvxplus_sim.plot_absorption(layers={"PM6_GSISO":80, "PVXplus1":80, "PVXplus2": 100})
gs_iso_2pvxplus_sim.plot_absorption(layers=gs_iso_2pvxplus_sim.find_max_current())


#%%% Triple junction with PM6:BTA3, PM6:GS-ISO and PVXplus

# Import from file
triple_junction = stacks.parse_external_stack("BTA3_GSISO_PVXplus_triple.txt")

# Create simulation object
triple_junction_sim = Simulation(triple_junction)
#Perform thickness variation
triple_junction_sim.thickness_variation({"BTA3":np.arange(40,80,10),
                                         "GSISO":np.arange(100, 190, 10),
                                         "PVXplus":np.arange(30, 60, 10)})

# Plot the current map
# triple_junction_sim.plot_current_map()
# Plot absorption at the combination with maximum current
triple_junction_sim.plot_absorption(layers=triple_junction_sim.find_max_current())

triple_junction_sim.print_row(triple_junction_sim.find_max_current())

#%%% Triple cell with PM6:IO4Cl, D18:Y6 and PVXplus

# Import from file
triple_junction = stacks.parse_external_stack("IO4Cl_D18Y6_PVXplus_triple.txt")

# Create simulation object
triple_junction_sim = Simulation(triple_junction)
#Perform thickness variation
triple_junction_sim.thickness_variation({"IO4Cl":np.arange(70,180,10),
                                         "D18Y6":np.arange(60, 130, 10),
                                         "PVXplus":np.arange(50, 120, 10)})


# Plot absorption at the combination with maximum current
triple_junction_sim.plot_absorption(layers=triple_junction_sim.find_max_current())

#%%% Triple cell with PM6:IO4Cl and 2 PVXplus

# Import from file
IO4Cl_2x_PVXplus = stacks.parse_external_stack("IO4Cl_2x_PVXplus_triple.txt")

# Create simulation object
IO4Cl_2x_PVXplus_sim = Simulation(IO4Cl_2x_PVXplus)
#Perform thickness variation
IO4Cl_2x_PVXplus_sim.thickness_variation({"IO4Cl":np.arange(70,180,10),
                                         "PVXplus1":np.arange(50, 120, 10),
                                         "PVXplus2":np.arange(50, 120, 10)})


# Plot absorption at the combination with maximum current
IO4Cl_2x_PVXplus_sim.plot_absorption(layers=IO4Cl_2x_PVXplus_sim.find_max_current())

#%%% Triple cell with PM6:GS-ISO, PM6:PCBM and PVXplus

# Import from file
GSISO_PCBM_PVXplus = stacks.parse_external_stack("GSISO_PCBM_PVXplus_triple.txt")

# Create simulation object
GSISO_PCBM_PVXplus_sim = Simulation(GSISO_PCBM_PVXplus)
#Perform thickness variation
GSISO_PCBM_PVXplus_sim.thickness_variation({"GSISO":np.arange(80,180,10),
                                         "PCBM":np.arange(60, 130, 10),
                                         "PVXplus":np.arange(50, 120, 10)})


# Plot absorption at the combination with maximum current
GSISO_PCBM_PVXplus_sim.plot_absorption(layers=GSISO_PCBM_PVXplus_sim.find_max_current())

#%%% Triple cell with PM6:GS-ISO, PM6:ITIC and PVXplus

# Import from file
GSISO_ITIC_PVXplus = stacks.parse_external_stack("GSISO_ITIC_PVXplus_triple.txt")

# Create simulation object
GSISO_ITIC_PVXplus_sim = Simulation(GSISO_ITIC_PVXplus)
#Perform thickness variation
GSISO_ITIC_PVXplus_sim.thickness_variation({"GSISO":np.arange(80,180,10),
                                         "ITIC":np.arange(60, 140, 10),
                                         "PVXplus":np.arange(50, 120, 10)})


# Plot absorption at the combination with maximum current
GSISO_ITIC_PVXplus_sim.plot_absorption(layers=GSISO_ITIC_PVXplus_sim.find_max_current())

#%%% Triple cell with PM6:GS-ISO, PM6:BTP-eC9 and PVXplus

# Import from file
GSISO_BTPeC9_PVXplus_triple = stacks.parse_external_stack("GSISO_BTPeC9_PVXplus_triple.txt")

# Create simulation object
GSISO_BTPeC9_PVXplus_triple_sim = Simulation(GSISO_BTPeC9_PVXplus_triple)
#Perform thickness variation
GSISO_BTPeC9_PVXplus_triple_sim.thickness_variation({"GSISO":np.arange(80,180,10),
                                         "BTPec9":np.arange(60, 140, 10),
                                         "PVXplus":np.arange(50, 120, 10)})


# Plot absorption at the combination with maximum current
GSISO_BTPeC9_PVXplus_triple_sim.plot_absorption(layers=GSISO_BTPeC9_PVXplus_triple_sim.find_max_current())

#%%% Triple cell with PM6:GS-ISO, PVXplus and PCE10:COi8DFIC

# Import from file
GSISO_PVXplus_Coi8_triple = stacks.parse_external_stack("GSISO_PVXplus_PCE10-Coi8.txt")

# Create simulation object
GSISO_PVXplus_Coi8_triple_sim = Simulation(GSISO_PVXplus_Coi8_triple)
#Perform thickness variation
GSISO_PVXplus_Coi8_triple_sim.thickness_variation({"GSISO":np.arange(80,180,10),
                                         "PVXplus":np.arange(50, 120, 10),
                                         "Coi8DFIC":np.arange(50, 120, 10)})


# Plot absorption at the combination with maximum current
GSISO_PVXplus_Coi8_triple_sim.plot_absorption(layers=GSISO_PVXplus_Coi8_triple_sim.find_max_current())

#%%% Triple cell with PM6:GS-ISO, PVXplus and PCE10:IEICO2F

# Import from file
GSISO_PVXplus_IEICO2F_triple = stacks.parse_external_stack("GSISO_PVXplus_PCE10-IEICO2F.txt")

# Create simulation object
GSISO_PVXplus_IEICO2F_triple_sim = Simulation(GSISO_PVXplus_IEICO2F_triple)
#Perform thickness variation
GSISO_PVXplus_IEICO2F_triple_sim.thickness_variation({"GSISO":np.arange(80,180,10),
                                         "PVXplus":np.arange(50, 120, 10),
                                         "IEICO2F":np.arange(50, 120, 10)})


# Plot absorption at the combination with maximum current
GSISO_PVXplus_IEICO2F_triple_sim.plot_absorption(layers=GSISO_PVXplus_IEICO2F_triple_sim.find_max_current())

#%%% Triple cell with PM6:GS-ISO, PM6:BTP-eC9 and PCE10:COi8DFIC

# Import from file
GSISO_BTPeC9_Coi8_triple = stacks.parse_external_stack("GSISO_BTPeC9_PCE10-Coi8.txt")

# Create simulation object
GSISO_BTPeC9_Coi8_triple_sim = Simulation(GSISO_BTPeC9_Coi8_triple)
#Perform thickness variation
GSISO_BTPeC9_Coi8_triple_sim.thickness_variation({"GSISO":np.arange(80,180,10),
                                         "BTPec9":np.arange(60, 140, 10),
                                         "Coi8DFIC":np.arange(50, 120, 10)})


# Plot absorption at the combination with maximum current
GSISO_BTPeC9_Coi8_triple_sim.plot_absorption(layers=GSISO_BTPeC9_Coi8_triple_sim.find_max_current())

#%%% Triple cell with PM6:GS-ISO, PM6:BTP-eC9 and PCE10:IEICO2F

# Import from file
GSISO_BTPeC9_IEICO2F_triple = stacks.parse_external_stack("GSISO_BTPeC9_PCE10-IEICO2F.txt")

# Create simulation object
GSISO_BTPeC9_IEICO2F_triple_sim = Simulation(GSISO_BTPeC9_IEICO2F_triple)
#Perform thickness variation
GSISO_BTPeC9_IEICO2F_triple_sim.thickness_variation({"GSISO":np.arange(80,180,10),
                                         "BTPec9":np.arange(60, 140, 10),
                                         "IEICO2F":np.arange(50, 120, 10)})


# Plot absorption at the combination with maximum current
GSISO_BTPeC9_IEICO2F_triple_sim.plot_absorption(layers=GSISO_BTPeC9_IEICO2F_triple_sim.find_max_current())

#%%% Triple cell with PBDBT:BTA3, PM6:GS-ISO, and PCE10:COi8DFIC

# Import from file
BTA3_GSISO_Coi8_triple = stacks.parse_external_stack("BTA3_GSISO_Coi8_triple.txt")

# Create simulation object
BTA3_GSISO_Coi8_triple_sim = Simulation(BTA3_GSISO_Coi8_triple)
#Perform thickness variation
BTA3_GSISO_Coi8_triple_sim.thickness_variation({"BTA3":np.arange(50,140,10),
                                         "GSISO":np.arange(80, 180, 10),
                                         "Coi8DFIC":np.arange(50, 140, 10)})


# Plot absorption at the combination with maximum current
BTA3_GSISO_Coi8_triple_sim.plot_absorption(layers=BTA3_GSISO_Coi8_triple_sim.find_max_current())

#%%% Triple cell with PBDBT:BTA3, PM6:GS-ISO, and PCE10:IEICO2F

# Import from file
BTA3_GSISO_IEICO2F_triple = stacks.parse_external_stack("BTA3_GSISO_IEICO2F_triple.txt")

# Create simulation object
BTA3_GSISO_IEICO2F_triple_sim = Simulation(BTA3_GSISO_IEICO2F_triple)
#Perform thickness variation
BTA3_GSISO_IEICO2F_triple_sim.thickness_variation({"BTA3":np.arange(50,140,10),
                                         "GSISO":np.arange(80, 180, 10),
                                         "IEICO2F":np.arange(50, 140, 10)})


# Plot absorption at the combination with maximum current
BTA3_GSISO_IEICO2F_triple_sim.plot_absorption(layers=BTA3_GSISO_IEICO2F_triple_sim.find_max_current())

#%%% Triple cell with PBDBT:BTA3, PM6:GS-ISO, and PM6:BTP-eC9-2Cl

# Import from file
BTA3_GSISO_BTP_triple = stacks.parse_external_stack("BTA3_GSISO_BTPeC9_triple.txt")

# Create simulation object
BTA3_GSISO_BTP_triple_sim = Simulation(BTA3_GSISO_BTP_triple)
#Perform thickness variation
BTA3_GSISO_BTP_triple_sim.thickness_variation({"BTA3":np.arange(50,140,10),
                                         "GSISO":np.arange(60, 180, 10),
                                         "BTPec9":np.arange(50, 140, 10)})


# Plot absorption at the combination with maximum current
BTA3_GSISO_BTP_triple_sim.plot_absorption(layers=BTA3_GSISO_BTP_triple_sim.find_max_current())


#%%% Triple cell with PBDBT:BTA3, PVXplus, and PCE10:COi8DFIC

# Import from file
BTA3_PVXplus_Coi8_triple = stacks.parse_external_stack("BTA3_PVXplus_Coi8_triple.txt")

# Create simulation object
BTA3_PVXplus_Coi8_triple_sim = Simulation(BTA3_PVXplus_Coi8_triple)
#Perform thickness variation
BTA3_PVXplus_Coi8_triple_sim.thickness_variation({"BTA3":np.arange(50,140,10),
                                         "PVXplus":np.arange(50, 120, 10),
                                         "Coi8DFIC":np.arange(50, 140, 10)})


# Plot absorption at the combination with maximum current
BTA3_PVXplus_Coi8_triple_sim.plot_absorption(layers=BTA3_PVXplus_Coi8_triple_sim.find_max_current())

#%%% Triple cell with PBDBT:BTA3, PVXplus, and PCE10:IEICO2F

# Import from file
BTA3_PVXplus_IEICO2F_triple = stacks.parse_external_stack("BTA3_PVXplus_IEICO2F_triple.txt")

# Create simulation object
BTA3_PVXplus_IEICO2F_triple_sim = Simulation(BTA3_PVXplus_IEICO2F_triple)
#Perform thickness variation
BTA3_PVXplus_IEICO2F_triple_sim.thickness_variation({"BTA3":np.arange(50,140,10),
                                         "PVXplus":np.arange(50, 120, 10),
                                         "IEICO2F":np.arange(50, 140, 10)})


# Plot absorption at the combination with maximum current
BTA3_PVXplus_IEICO2F_triple_sim.plot_absorption(layers=BTA3_PVXplus_IEICO2F_triple_sim.find_max_current())

#%%% Triple cell with PBDBT:BTA3, PVXplus, and PVXplus

# Import from file
BTA3_PVXplus_PVXplus_triple = stacks.parse_external_stack("BTA3_PVXplus_PVXplus_triple.txt")

# Create simulation object
BTA3_PVXplus_PVXplus_triple_sim = Simulation(BTA3_PVXplus_PVXplus_triple)
#Perform thickness variation
BTA3_PVXplus_PVXplus_triple_sim.thickness_variation({"BTA3":np.arange(50,140,10),
                                         "PVXplus1":np.arange(50, 120, 10),
                                         "PVXplus2":np.arange(50, 120, 10)})


# Plot absorption at the combination with maximum current
BTA3_PVXplus_PVXplus_triple_sim.plot_absorption(layers=BTA3_PVXplus_PVXplus_triple_sim.find_max_current())

#%%% Triple cell with PBDBT:BTA3, PM6:ITIC, and PVXplus

# Import from file
BTA3_ITIC_PVXplus_triple = stacks.parse_external_stack("BTA3_ITIC_PVXplus_triple.txt")

# Create simulation object
BTA3_ITIC_PVXplus_triple_sim = Simulation(BTA3_ITIC_PVXplus_triple)
#Perform thickness variation
BTA3_ITIC_PVXplus_triple_sim.thickness_variation({"BTA3":np.arange(50,140,10),
                                         "ITIC":np.arange(50, 150, 10),
                                         "PVXplus":np.arange(50, 130, 10)})


# Plot absorption at the combination with maximum current
BTA3_ITIC_PVXplus_triple_sim.plot_absorption(layers=BTA3_ITIC_PVXplus_triple_sim.find_max_current())

BTA3_ITIC_PVXplus_triple_sim.print_row(BTA3_ITIC_PVXplus_triple_sim.find_max_current())

#%%% Triple cell with PBDBT:BTA3, GSISO, and BTPeC9

# Import from file
BTA3_GSISO_BTP_triple = stacks.parse_external_stack("BTA3_GSISO_BTPeC9_triple.txt")

# Create simulation object
BTA3_GSISO_BTP_triple_sim = Simulation(BTA3_GSISO_BTP_triple)
#Perform thickness variation
BTA3_GSISO_BTP_triple_sim.thickness_variation({"BTA3":np.arange(50,140,10),
                                         "GSISO":np.arange(50, 180, 10),
                                         "BTPec9":np.arange(50, 120, 10)})


# Plot absorption at the combination with maximum current
BTA3_GSISO_BTP_triple_sim.plot_absorption(layers=BTA3_GSISO_BTP_triple_sim.find_max_current())


#%%% Triple cell with PBDBT:BTA3, PM6:BTPeC9, and PVXplus

# Import from file
BTA3_BTPeC9_PVXplus_triple = stacks.parse_external_stack("BTA3_BTPeC9_PVXplus_triple.txt")

# Create simulation object
BTA3_BTPeC9_PVXplus_triple_sim = Simulation(BTA3_BTPeC9_PVXplus_triple)
#Perform thickness variation
BTA3_BTPeC9_PVXplus_triple_sim.thickness_variation({"BTA3":np.arange(50,140,10),
                                         "BTPec9":np.arange(50, 120, 10),
                                         "PVXplus":np.arange(50, 120, 10)})


# Plot absorption at the combination with maximum current
BTA3_BTPeC9_PVXplus_triple_sim.plot_absorption(layers=BTA3_BTPeC9_PVXplus_triple_sim.find_max_current())

#%%% Triple cell with PBDBT:BTA3, PM6:GS-ISO, and PM6:PCBM

# Import from file
BTA3_GSISO_PCBM_triple = stacks.parse_external_stack("BTA3_GSISO_PCBM_triple.txt")

# Create simulation object
BTA3_GSISO_PCBM_triple_sim = Simulation(BTA3_GSISO_PCBM_triple)
#Perform thickness variation
BTA3_GSISO_PCBM_triple_sim.thickness_variation({"BTA3":np.arange(30,70,10),
                                         "GSISO":np.arange(30, 70, 10),
                                         "PCBM":np.arange(50, 150, 10)})


# Plot absorption at the combination with maximum current
BTA3_GSISO_PCBM_triple_sim.plot_absorption(layers=BTA3_GSISO_PCBM_triple_sim.find_max_current())
# Print the values at the maximum current point
BTA3_GSISO_PCBM_triple_sim.print_row(BTA3_GSISO_PCBM_triple_sim.find_max_current())

#%%% Triple cell with 3 PVXplus subcells

# Import from file
PVXplus_homo_triple = stacks.parse_external_stack("PVXplus_homo_triple.txt")

# Create simulation object
PVXplus_homo_triple_sim = Simulation(PVXplus_homo_triple)
#Perform thickness variation
PVXplus_homo_triple_sim.thickness_variation({"PVXplus1":np.arange(50,120,10),
                                         "PVXplus2":np.arange(50, 120, 10),
                                         "PVXplus3":np.arange(50, 120, 10)})


# Plot absorption at the combination with maximum current
PVXplus_homo_triple_sim.plot_absorption(layers=PVXplus_homo_triple_sim.find_max_current())

#%%% Triple cell with PBDB-T:BTA3, D18:FCC-Cl and PVXplus

# Import from file
triple_junction = stacks.parse_external_stack("BTA3_D18FCC_PVXplus_triple.txt")

# Create simulation object
triple_junction_sim = Simulation(triple_junction)
#Perform thickness variation
triple_junction_sim.thickness_variation({"BTA3":np.arange(30,100,10),
                                         "D18FCC":np.arange(180, 300, 10),
                                         "PVXplus":np.arange(180, 300, 10)})


# Plot absorption at the combination with maximum current
triple_junction_sim.plot_absorption(layers=triple_junction_sim.find_max_current())
# Print the values at the maximum current point
triple_junction_sim.print_row(triple_junction_sim.find_max_current())

#%% 4-junction simulations

#%%% 4-junction PVXplus
# Import from file
PVXplus_homo_4junction = stacks.parse_external_stack("PVXplus_homo_4-junction.txt")

# Create simulation object
PVXplus_homo_4junction_sim = Simulation(PVXplus_homo_4junction)
#Perform thickness variation
PVXplus_homo_4junction_sim.thickness_variation({"PVXplus1":np.arange(30,60,10),
                                         "PVXplus2":np.arange(30, 60, 10),
                                         "PVXplus3":np.arange(60, 100, 10),
                                         "PVXplus4":np.arange(80, 120, 10)})


# Plot absorption at the combination with maximum current
PVXplus_homo_4junction_sim.plot_absorption(layers=PVXplus_homo_4junction_sim.find_max_current())

#%%% 4-junction with PM6:BTA3, PM6:BTPeC92Cl, PVXplus and PTB7-Th:IEICO2F
# Import from file
A_4junction = stacks.parse_external_stack("BTA3-BTP-PVXplus-IEICO4F_4-junction.txt")

# Create simulation object
A_4junction_sim = Simulation(A_4junction)
#Perform thickness variation
A_4junction_sim.thickness_variation({"BTA3":np.arange(50,140,10),
                                         "BTPec9":np.arange(50, 120, 10),
                                         "PVXplus":np.arange(60, 100, 10),
                                         "IEICO2F":np.arange(50, 140, 10)})


# Plot absorption at the combination with maximum current
A_4junction_sim.plot_absorption(layers=A_4junction_sim.find_max_current())

#%%% 4-junction with PM6:BTA3 x2 time and PVXplus x2 times
# Import from file
B_4junction = stacks.parse_external_stack("BTA3x2_PVXplusx2_4-junction.txt")

# Create simulation object
B_4junction_sim = Simulation(B_4junction)
#Perform thickness variation
B_4junction_sim.thickness_variation({"BTA3":np.arange(50,140,10),
                                         "BTA3_2":np.arange(50, 140, 10),
                                         "PVXplus":np.arange(50, 120, 10),
                                         "PVXplus2":np.arange(50, 120, 10)})


# Plot absorption at the combination with maximum current
B_4junction_sim.plot_absorption(layers=B_4junction_sim.find_max_current())

#%%% 4-junction with PM6:BTA3, PM6:BTPeC92Cl, PVXplus and PVXplus
# Import from file
B_4junction = stacks.parse_external_stack("BTA3-BTP-PVXplus-PVXplus_4-junction.txt")

# Create simulation object
B_4junction_sim = Simulation(B_4junction)
#Perform thickness variation
B_4junction_sim.thickness_variation({"BTA3":np.arange(50,140,10),
                                         "BTPec9":np.arange(50, 120, 10),
                                         "PVXplus":np.arange(50, 120, 10),
                                         "PVXplus1":np.arange(50, 120, 10)})


# Plot absorption at the combination with maximum current
B_4junction_sim.plot_absorption(layers=B_4junction_sim.find_max_current())

#%%% 4-junction with PM6:BTA3 and PVXplus x3
# Import from file
B_4junction = stacks.parse_external_stack("BTA3_PVXplusx3_4-junction.txt")

# Create simulation object
B_4junction_sim = Simulation(B_4junction)
#Perform thickness variation
B_4junction_sim.thickness_variation({"BTA3":np.arange(50,140,10),
                                         "PVXplus":np.arange(50, 130, 10),
                                         "PVXplus1":np.arange(50, 130, 10),
                                         "PVXplus2":np.arange(50, 130, 10)})


# Plot absorption at the combination with maximum current
B_4junction_sim.plot_absorption(layers=B_4junction_sim.find_max_current())