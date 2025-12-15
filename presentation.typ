// --- THEME CONFIGURATION ---
#let bg-color = rgb("#1e1e2e") 
#let text-color = rgb("#cdd6f4")
#let accent-color = rgb("#f38ba8") 
#let math-color = rgb("#89b4fa") // Light Blue for Math

#set page(
  paper: "presentation-16-9",
  fill: bg-color,
  margin: (x: 1.5cm, y: 1.5cm)
)
#set text(
  font: "Linux Libertine",
  size: 20pt,
  fill: text-color
)

// Apply math color
#show math.equation: set text(fill: math-color)

// Define missing symbols
#let hbar = math.planck.reduce

// --- SLIDE FUNCTION ---
#let slide(title: none, body) = {
  if title != none {
    text(28pt, weight: "bold", fill: accent-color)[#title]
    v(0.2em)
    line(length: 100%, stroke: 2pt + text-color)
    v(0.8em)
  }
  body
  pagebreak()
}

// --- TITLE SLIDE (ICAP 2025) ---
#align(center + horizon)[
  #text(32pt, weight: "bold", fill: accent-color)[Robust Quantum Spin Hall State in Monolayer 1T'-WTe#sub[2]]
  #v(1em)
  #text(22pt)[*Shahriar Pollob*]
  #v(0.2em)
  #text(18pt, style: "italic")[Supervised by M. Shahnoor Rahman]
  #v(2em)
  #line(length: 60%, stroke: 1pt + text-color)
  #v(0.5em)
  #text(18pt)[Presented at *ICAP 2025*] \
  #text(16pt)[International Conference on Advances in Physics] \
  #text(16pt)[Shahjalal University of Science and Technology (SUST)]
]
#pagebreak()

// --- SLIDE 2: THE CONCEPT (For General Audience) ---
#slide(title: "What is a Topological Insulator?")[
  Standard insulators have a global energy gap. *Topological Insulators (TIs)* are distinct: they are insulating in the bulk but conducting at the edges.
  
  #grid(
    columns: (1.5fr, 1fr),
    gutter: 20pt,
    [
      *The Mechanism: Band Inversion*
      Driven by strong *Spin-Orbit Coupling (SOC)*, the conduction and valence bands swap character (parity).
      
      *The Hamiltonian:*
      $ H = H_0 + underbrace(lambda_("SOC") vec(L) dot vec(S), "Topological Driver") $
      
      This inversion creates a non-trivial winding number ($Z_2=1$), necessitating gapless edge states.
    ],
    align(center)[
      // Placeholder for a concept diagram if you had one, 
      // otherwise we use the structure to show the material
      #image("figures/Fig_Structure_Views_V2.png", width: 80%)
      #text(14pt)[1T'-WTe2 Crystal Structure]
    ]
  )
]

// --- SLIDE 3: METHODOLOGY (The Math) ---
#slide(title: "Computational Framework")[
  We characterize the topology using *Density Functional Theory (DFT)* and *Wannier Interpolation*.
  
  *1. First-Principles Hamiltonian (DFT):*
  Solving the Kohn-Sham equations with relativistic pseudopotentials (PBE + SOC):
  $ [ -hbar^2 / (2m) nabla^2 + V_(eff)(vec(r)) ] psi_i = epsilon_i psi_i $
  
  *2. Topological Invariant (Kubo Formula):*
  The Spin Hall Conductivity (SHC) is calculated via the Berry Curvature $Omega_{n}(vec(k))$:
  
  $ sigma_(xy)^(spin) = e^2 / hbar sum_n integral_(BZ) (d^2k) / ((2 pi)^2) f_n(vec(k)) Omega_(n,xy)^(spin)(vec(k)) $
  
  *Tools:* Quantum ESPRESSO $arrow$ Wannier90 $arrow$ PostW90
]

// --- SLIDE 4: ELECTRONIC STRUCTURE ---
#slide(title: "Results: Band Inversion")[
  The 1T' structural distortion induces a semimetallic ground state, but the *direct gap* opens due to SOC.
  
  #grid(
    columns: (1fr, 1fr),
    gutter: 10pt,
    align(center)[
      #image("figures/Fig1_BandStructure_Final.png", height: 70%)
      #v(-0.5em)
      #text(16pt)[Relativistic Band Structure]
    ],
    align(center)[
      #image("figures/Fig_PDOS_Inversion.png", height: 70%)
      #v(-0.5em)
      #text(16pt)[Orbital Mixing ($d-p$ Inversion)]
    ]
  )
  *Observation:* The W-$d$ and Te-$p$ bands invert near $Gamma$, a signature of the QSH phase.
]

// --- SLIDE 5: TOPOLOGICAL PROOF (SHC) ---
#slide(title: "Proof 1: Spin Hall Conductivity")[
  We calculate the intrinsic SHC using the Kubo-Greenwood formula.
  
  #grid(
    columns: (1.2fr, 1fr),
    gutter: 20pt,
    align(center)[
      #image("figures/Fig2_SHC_Final.png", width: 100%)
    ],
    align(horizon)[
      *The Result:*
      - A quantized plateau appears in the bulk gap.
      - Value: $sigma_(xy) approx 2 e^2 / h$ (Conductance Quantum).
      
      *Implication:*
      This non-zero invariant confirms the *Quantum Spin Hall* state ($Z_2 = 1$).
    ]
  )
]

// --- SLIDE 6: TOPOLOGICAL PROOF (RIBBON) ---
#slide(title: "Proof 2: Helical Edge States")[
  *Bulk-Boundary Correspondence:* If the bulk is topological, the boundary must be metallic.
  
  #grid(
    columns: (1fr, 1.5fr),
    gutter: 20pt,
    align(horizon)[
      *Simulation:*
      - 30-Unit Cell Ribbon.
      - Constructed from Maximally Localized Wannier Functions.
      
      *Observation:*
      - *Red States:* Gapless modes crossing the Fermi level.
      - These are the topologically protected edge channels.
    ],
    align(center)[
      #image("figures/Fig_Ribbon_EdgeStates.png", width: 85%)
    ]
  )
]

// --- SLIDE 7: CONCLUSION ---
#slide(title: "Summary")[
  - *Conclusion:*
    - We have robustly characterized monolayer 1T'-WTe#sub[2] as a QSH insulator.
    - Verified via orbital inversion, quantized SHC, and edge states.
    - Established a reproducible workflow for topological materials.

  - *Future Work:*
    - Investigation of strain tuning and electric field effects.
]
