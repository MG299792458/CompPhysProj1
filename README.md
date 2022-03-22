# Molecular dynamics simulation of Argon atoms
The contents of the repository allow for the simulation of Argon in it's solid, liquid or gaseous form.
All the tools are present to build your own simulation or you can run a pre-existing one from the `simulations` subfolder.

## Table of contents
[[_TOC_]]

## Installation
Installation of a module is not needed, place the `skeleton.py` file in the same folder as your working file and use

```python
from skeleton import *
```
to access the necessary functions and constants.

## Usage

```python
from skeleton import (
    init_fcc, equalise_system, Verlet_integrate_images,
    gen_rv_matrices, store_rv,
    SIGMA, pair_correlation
)

#Define constants
dimensions = 3      # Number of dimension in the simulation volume
box_length = 4      # Length of the sides of the box simulation volume
intv_steps = 1200   # Number of timesteps to Verlet integrate
syst_tempk = 70     # Temperature of system in Kelvin
fcc_spacin = 1.4    # Spacing between FCC lattice unit cells
ar_parts_m = 1      # Argon particle mass in dimensionless units
time_const = 1e-2   # Integration time between to subsequent timesteps

# Create the initial conditions for the simulation
r0, v0 = init_fcc(box_length,
                fcc_spacin,
                0,              # Offset from origin of cube
                syst_temp
                )

# Create the arrays that store the results
R, V = gen_rv_matrices(dimensions, num_part, intv_steps)
R, V = store_rv(R, V, r0, v0, 0)    # Store the initial conditions at the first timestep

# Let the simulation run!
Rt, Vt, forces, potentials = Verlet_integrate_images(num_part, R, V, ar_part_m,
                                intv_steps, 0, box_length, dimensions, timespacing)

# Inspect a range of observables one of which is the pair correlation function:
counts, bins = pair_correlation(Rt, bin_amnt=200, box_length)
```

## Contributors

@sangersjeroen
@agefrancke2
@mwglorie
