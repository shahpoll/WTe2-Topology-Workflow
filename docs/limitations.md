# Limitations & Future Outlook

# Computational Constraints & Approximations

This section outlines the methodological limitations inherent to the Density Functional Theory (DFT) implementation and the Wannier interpolation scheme.

## 1. Functional-Dependent Gap Underestimation
The primary limitation of the Generalized Gradient Approximation (PBE) is the systematic underestimation of the semiconductor band gap. In the case of 1T'-WTe₂, this results in a semimetallic ground state ($E_g < 0$) rather than the experimentally observed small gap ($\approx 55$ meV). However, the *direct* gap at the band inversion point remains open, ensuring the topological invariant ($Z_2$) is physically well-defined. The topological gap is qualitatively correct ($Z_2=1$) but the magnitude is likely underestimated compared to hybrid functional (HSE06) results.

## Dimensionality & Coulomb Cutoff
- **Limitation:** A standard 3D periodic solver was used with high vacuum (~17.6 Å).
- **Refinement:** We did not employ a 2D Coulomb cutoff (e.g., `assume_isolated='2D'`). Long-range van der Waals interactions between periodic images are assumed negligible but not explicitly truncated.

## Finite-Temperature Stability
- **Limitation:** Calculations correspond to $T=0$ K.
- **Outlook:** The topological protection is robust, but phonon stability and electron-phonon scattering at room temperature were not simulated.
