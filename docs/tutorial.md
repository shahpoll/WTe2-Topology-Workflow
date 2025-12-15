# Computational Execution Protocol

This document details the step-by-step procedure for reproducing the topological invariant calculation. The workflow proceeds from the Density Functional Theory (DFT) ground state to the Wannierized tight-binding model.

## Step 1: Self-Consistent Field (SCF)
Run the ground state calculation to converge the charge density.
```bash
mpirun -np 40 pw.x < wte2.scf.in
```
*Goal:* Converge in < 50 steps.

## Step 2: Wannierization
We use a frozen window of $[-10, 2]$ eV to disentangle the topological bands.
```bash
wannier90.x -pp wte2
mpirun -np 40 pw2wannier90.x < wte2.pw2wan.in
wannier90.x wte2
```
*Check:* Look at `wte2.wout`. Ensure spreads converge to $< 30 \AA^2$.

## Step 3: Topological Proofs
Run the python scripts to generate the observables.

### Spin Hall Conductivity
```bash
python plot_shc.py
```

### Ribbon Edge States
```bash
python plot_ribbon.py
```
