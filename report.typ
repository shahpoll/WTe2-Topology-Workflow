// --- DOCUMENT SETUP ---
#set document(title: "Topological Characterization of 1T'-WTe2", author: "Shahriar Pollob")
#set page(
  paper: "a4",
  margin: (x: 2cm, y: 2cm),
  numbering: "1",
)
#set text(font: "Linux Libertine", size: 11pt)
#set heading(numbering: "1.1")
#show heading: it => [
  #v(0.5em)
  #text(weight: "bold", size: 13pt, it)
  #v(0.3em)
]

// --- TITLE ---
#align(center)[
  #text(18pt, weight: "bold")[Topological Characterization of Monolayer 1T'-WTe#sub[2]]
  #v(0.5em)
  #text(13pt)[Shahriar Pollob] \
  #text(11pt, style: "italic")[Supervised by M. Shahnoor Rahman] \
  #v(0.5em)
  #text(10pt)[Generated via Quantum ESPRESSO & Wannier90 Workflow]
  #line(length: 100%, stroke: 0.5pt + gray)
  #v(1cm)
]

// --- ABSTRACT ---
= Abstract
We present a complete computational characterization of the Quantum Spin Hall (QSH) phase in monolayer 1T'-WTe#sub[2]. Utilizing a fully relativistic PBE+SOC framework, we demonstrate the robustness of the $Z_2=1$ topological invariant. The topological phase is verified through two complementary observables: the quantized Spin Hall Conductivity (SHC) plateau and the existence of helical edge states in a ribbon geometry. This document serves as a comprehensive report of the methodology, validation, and physical results.

// --- 1. INTRODUCTION & PHYSICS ---
= Introduction: The Topological Mechanism
Monolayer Tungsten Ditelluride (1T'-WTe#sub[2]) is a transition metal dichalcogenide that exhibits a Quantum Spin Hall (QSH) state. Unlike the semiconducting 2H phase, the 1T' phase is structurally distorted (Peierls distortion), leading to a band inversion between the Tungsten $d$-orbitals and Tellurium $p$-orbitals.



As shown in Figure 2, the W-$d$ states (blue) dip below the Te-$p$ states (orange) near the Fermi level. This orbital inversion, combined with strong Spin-Orbit Coupling (SOC), opens a fundamental gap characteristic of the $Z_2=1$ topological phase.

// --- 2. COMPUTATIONAL METHODS ---
= Computational Methods


#figure(
  table(
    columns: (auto, auto),
    inset: 10pt,
    align: horizon,
    fill: (_, row) => if calc.odd(row) { luma(240) } else { white },
    [*Parameter*], [*Value*],
    "Lattice Constants", "a=3.49 Å, b=6.33 Å",
    "Vacuum Spacing", "~17.6 Å",
    "Plane Wave Cutoff", "60 Ry (Wfc) / 720 Ry (Rho)",
    "K-Mesh (NSCF)", "12 x 6 x 1",
    "Wannier Window", "Frozen: [-10, 2.0] eV",
    "Smearing", "Marzari-Vanderbilt (14 meV)"
  ),
  caption: [Simulation Parameters]
)

// --- 3. ELECTRONIC STRUCTURE ---
= Electronic Structure
The relativistic band structure (Figure 3) reveals the SOC-induced gap opening at the $Gamma$ point. While the PBE functional predicts a semimetallic ground state (negative indirect gap), the direct gap responsible for the topology remains open and inverted.

#figure(
  image("figures/Fig1_BandStructure_Final.png", width: 85%),
  caption: [Relativistic Band Structure showing the inverted gap.]
)

// --- 4. TOPOLOGICAL INVARIANT ---
= Topological Verification ($Z_2 = 1$)
We verify the non-trivial topology using two distinct methods.

== 4.1 Spin Hall Conductivity (SHC)
The intrinsic Spin Hall Conductivity $sigma_("xy")^("spin")$ was calculated via the Kubo formula. Figure 4 shows a quantized plateau within the bulk gap, a definitive signature of the QSH state.

#figure(
  image("figures/Fig2_SHC_Final.png", width: 85%),
  caption: [Quantized Spin Hall Conductivity Plateau.]
)

== 4.2 Bulk-Boundary Correspondence (Edge States)
To visualize the boundary physics, we constructed a tight-binding Hamiltonian for a 30-unit-cell ribbon. Diagonalization reveals gapless helical edge states (red lines in Figure 5) connecting the valence and conduction bands.

#figure(
  image("figures/Fig_Ribbon_EdgeStates.png", width: 75%),
  caption: [Helical Edge States traversing the bulk gap.]
)

// --- 5. VALIDATION & QUALITY CONTROL ---
= Validation & Reproducibility
To ensure numerical robustness, we verified the convergence of the Wannier minimization. The total spread converged to $< 30 \AA^2$, indicating well-localized functions.

#figure(image("figures/Fig_Credibility_Spreads.png", width: 85%), caption: [Spread Convergence])

#figure(image("figures/validation_dft_vs_wannier.png", width: 85%), caption: [DFT vs Wannier Overlay])

= Reproducibility Pipeline
The entire workflow is automated via the scripts provided in the attached repository.

#figure(
  image("figures/Fig_Workflow.png", width: 90%),
  caption: [Computational Workflow]
)
