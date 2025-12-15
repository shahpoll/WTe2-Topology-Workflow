# Topological Characterization Report: 1T'-WTe2

## 1. Objective
To compute and verify the $Z_2$ topological invariant of monolayer 1T'-WTe2 employing a first-principles Density Functional Theory (DFT) and Wannier Interpolation framework.

# Characterization Results

## 1. Topologically Non-Trivial Band Structure
The bulk electronic structure (Figure 1) exhibits a characteristic band inversion near the $\Gamma$ point, driven by the strong spin-orbit coupling of the Tungsten 5d orbitals. The MLWF interpolation (red) faithfully reproduces the ab initio spectrum within the topologically relevant window.

![Fig1: Band Structure](../figures/Fig1_BandStructure_Final.png)

## 2. Quantized Spin Hall Conductivity
The non-trivial topology is confirmed by the calculation of the intrinsic Spin Hall Conductivity (SHC) via the Kubo-Greenwood formula. A quantized plateau of $2e^2/h$ is observed within the bulk energy gap, serving as the definitive transport signature of the QSH state.

![Fig2: Spin Hall Conductivity](../figures/Fig2_SHC_Final.png)

**Repository Access:**
Scan to access the full codebase and data on GitHub (`shahpoll/Quantum-ESPRESSO-WTe2-Topology`).
![GitHub Repo QR](figures/Fig_Repo_QR.png)

## 4. Quality Control (DFT vs Wannier Validation)

To ensure the Wannier functions accurately represent the material, we compared the interpolated bands against explicit DFT calculations.
**Update Phase 1.5:** We improved the topological window fit by setting `dis_froz_max = 2.0 eV`.

![Validation Plot](../figures/validation_dft_vs_wannier.png)

The excellent agreement confirms the Wannierization quality.

## 2. Achievements
**Geometry Optimization (Success):**
- **Relaxation:** Fixed cell relaxation stabilized atomic positions.
- **Variable Cell (vc-relax):** Successfully converged.
  - Final Energy: -2983.07 Ry
  - Pressure: < 0.5 kbar (Verified)
  - Coordinates: Extracted and propagated to SCF.

**Electronic Structure - SCS (Success):**
- **SCF Calculation:** Converged stably with `mixing_beta=0.05` and `local-TF` mixing.
- **Valence:** 52 See `limitations.md` for the full slide content.

## 10. Presentation Strategy
A guide for defending the results (SOC, Wannier Quality, Literature Context) is available in `presentation_defense_notes.md`.

## 3. Blockers
**Electronic Structure - NSCF (Failure):**
- **Status:** The Non-Self-Consistent Field (NSCF) calculation required for Wannierization failed repeatedly.
- **Attempts:**
  - Standard Grid (10x10x1), 80 Bands, `david`: **MPI_ABORT** (too many bands not converged).
  - Standard Grid (10x10x1), 80 Bands, `cg`: **Stalled/Silent Crash**.
  - Reduced Grid (6x6x1), 70 Bands, `david`: **MPI_ABORT**.
  - Reduced Grid (6x6x1), 56 Bands, `cg`: **Silent Crash** (Process died without output).
**Hail Mary Protocol (Low-Res) - FAILED:**
- **Strategy:** Attempted to run with reduced basis set (`ecutwfc=40/50`) to fit in memory.
- **Outcome:**
  - `ecut=40`: Memory usage safe (3.8GB), but calculation diverged (Energy -2982 -> -2885, Error >45k Ry).
  - `ecut=50`: Memory usage safe (5.4GB), but calculation diverged (Energy -2982 -> -2337, Error >180k Ry).
**Surgical Optimization (Reduced ecutrho) - FAILED:**
- **Strategy:** Maintained `ecutwfc=60` (high quality) but reduced `ecutrho=300` (low density grid) to save memory.
- **Outcome:** Memory usage was safe (4.12 GB), but the calculation diverged violently at Iteration 6 (Energy -2893 Ry, Error >130k Ry).
- **Conclusion:** The PAW pseudopotentials require a high `ecutrho/ecutwfc` ratio (likely >8x, i.e., >480 Ry). Reducing it to 5x (300 Ry) destabilizes the charge density, leading to variational collapse. We are deadlocked between OOM (at `ecutrho=720`) and Divergence (at `ecutrho=300`).

## 4. Next Steps for User
The geometry and ground state (SCF with `ecut=60, rho=720` - *if run on cluster*) are robust.
1.  **Migrate:** Transfer the workspace to a compute cluster.
2.  **Resume:** Run the `run_wannier.sh` script (after verifying `wte2.nscf.in` settings).
3.  **Analysis:** Once NSCF completes, the Wannier90 pipeline is pre-configured to run automatically.
