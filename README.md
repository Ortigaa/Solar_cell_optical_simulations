# Transfer Matrix Optical and Current Simulation Tool for Solar Cells

This repository contains a Python-based optical simulation toolkit designed to calculate absorption spectra and short-circuit current density ($J_{sc}$) in various solar cell architectures (single-junction, tandem, and multi-junction stacks). The calculations are performed using the Transfer-Matrix Method (TMM).

The project was developed for academic research to model layer-dependent absorption, evaluate thickness optimizations, and compute current generation under standard solar and indoor illumination sources.

---

## Technical Overview

The framework relies on calculating the transfer matrix across thin-film stack boundaries to compute layer-by-layer optical absorption, reflection, and transmission profiles.

Key functionality includes:
* **Optical Absorptance Calculations:** Uses standard transfer matrix formulations (`tmm`) to simulate wave propagation through arbitrary multi-layer structures.
* **Current Density Evaluation:** Integrates optical absorption against incoming spectral photon flux (e.g., AM1.5G or indoor LED spectra) and optional External Quantum Efficiency (EQE) spectrum functions to determine photogenerated current densities ($J_{sc}$).
* **Thickness Sweeps & Optimization:** Evaluates 1D and 2D thickness variation spaces to locate combinations yielding optimal current output.
* **Data Export & Visualization:** Generates absorption spectra profiles, 2D current contour maps, and exports calculated datasets to plain-text formats.

---

## Repository Structure

* **`main.py`**: Primary entry point containing test cases and simulation workflows for single-junction, tandem (2-junction), 3-junction, and 4-junction solar cells.
* **`stack_simulation.py`**: Defines the `Simulation` class responsible for spectrum interpolation, TMM core integration, sweep management, and plot generation.
* **`stacks.py`**: Defines the `Stack` structure and provides routines for parsing stack setup files as well as loading complex refractive index databases ($n, k$).
* **`functions.py`**: Auxiliary routines for converting spectral irradiance (W·m⁻²·nm⁻¹) to photon flux density.
* **`extract_n_and_a.py`**: Pre-processing script for separating wavelength, refractive index ($n$), attenuation coefficient ($k$), and calculating absorption coefficients ($a$).

### Expected Directory Layout

The scripts rely on the following subfolder structure for reading input data and exporting output:

```text
.
├── output/                     # Export directory for calculated data files
├── EQE/                        # Measured External Quantum Efficiency spectra files
├── nk_values/                  # Material refractive index data files
├── stacks/                     # Text configuration files for stack definitions
├── sun_scout.csv               # AM1.5G reference solar spectrum
├── test_LED_warm_500lux.txt   # Low-light spectrum dataset
├── extract_n_and_a.py
├── functions.py
├── main.py
├── stack_simulation.py
└── stacks.py
```

---

## Dependencies and Installation

The toolkit relies on standard Python scientific packages.

### Requirements

* Python 3.8+
* `numpy`
* `scipy`
* `matplotlib`
* `pandas`
* `tmm`

### Installation

Install all required dependencies using `pip`:

```bash
pip install numpy scipy matplotlib pandas tmm
```

---

## Usage Example

Execute pre-configured simulation sequences via `main.py`:

```bash
python main.py
```

Alternatively, initialize and run custom stack calculations within a Python script:

```python
import numpy as np
import stacks
from stack_simulation import Simulation

# Option A: Load a predefined stack structure from stacks.py
cell_stack = stacks.single_PVXplus

# Option B: Parse a stack setup from a plain text file in the stacks/ directory
# cell_stack = stacks.parse_external_stack("BTA3_PVXplus_tandem.txt")

# Initialize simulation under AM1.5G illumination ("AM15" or "LowLight")
sim = Simulation(cell_stack, light_source="AM15")

# Run a thickness variation sweep across target absorber layers (thicknesses in nm)
sim.thickness_variation({"PVXplus": np.arange(50, 100, 5)})

# Find optimal layer thicknesses maximizing current density
optimal_thicknesses = sim.find_max_current()

# Plot spectral absorption for the optimal combination
sim.plot_absorption(layers=optimal_thicknesses, export=True)
```

---

## Stack File Specification

When parsing external stack definitions from the `stacks/` directory (e.g., `parse_external_stack`), files must adhere to the following structured format:

```text
Description
Layer structure description here

Stack
air	inf	1
glass	1100000	nk_glass
ITO	185	nk_ITO_185_nm
ActiveLayer	100	nk_material_active
Ag	100	nk_Ag
air2	inf	1
```

Each row under the `Stack` header consists of tab-separated values specifying:
1. **Layer Name:** Identifier string.
2. **Thickness:** Layer thickness in nanometers (`inf` for semi-infinite ambient layers).
3. **nk Key:** Corresponding filename identifier matching data loaded from `nk_values/` (or `1` for air/vacuum).

---

## License

This project is made available for academic, educational, and research purposes.