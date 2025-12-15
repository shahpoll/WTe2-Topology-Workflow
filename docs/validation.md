# Numerical Verification & Stability Analysis

Ensuring the fidelity of the topological characterization requires rigorous validation of the interpolated electronic structure. This section documents the convergence checks and basis set accuracy.
![Spreads](../artifacts/Fig_Credibility_Spreads.png)
*Fig 1: Wannier Spread Convergence (< 30 Ang^2).*

## 2. Band Overlay (The "Accuracy" Check)
Comparing DFT eigenvalues (black) with Wannier interpolation (red).
![Overlay](../artifacts/validation_dft_vs_wannier.png)
*Fig 2: Perfect overlay validates the model parameters and window selection.*

## 3. Methods Table
Summary of computational parameters.

| Parameter | Value |
| :--- | :--- |
| **Functional** | PBE (Fully Relativistic) |
| **Pseudopotentials** | `W.rel-pbe...UPF`, `Te.rel-pbe...UPF` |
| **Cutoffs** | 60Ry (wfc) / 720Ry (rho) |
| **K-Mesh (SCF)** | $12 \times 12 \times 1$ |
| **K-Mesh (Wannier)** | $10 \times 10 \times 1$ |
| **Wannier Bands** | 72 DFT Bands $\rightarrow$ 44 Wannier Functions |
| **Fitting Window** | $[-10.0, 2.0]$ eV |
| **Vacuum** | 17.6 Å |
