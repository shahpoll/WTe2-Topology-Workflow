// --- THEME CONFIGURATION ---
// Dark "Developer/Hacker" Aesthetic
#let bg-color = rgb("#1e1e2e") 
#let text-color = rgb("#cdd6f4")
#let accent-color = rgb("#f38ba8") // Red/Pink
#let math-color = rgb("#89b4fa")   // Blue

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

// --- SLIDE TEMPLATE ---
#let slide(title: none, body) = {
  if title != none {
    text(26pt, weight: "bold", fill: accent-color)[#title]
    v(0.2em)
    line(length: 100%, stroke: 2pt + text-color)
    v(0.8em)
  }
  body
  pagebreak()
}

// --- SLIDE 1: TITLE (OFFICIAL ACCEPTED) ---
#align(center + horizon)[
  #text(26pt, weight: "bold", fill: accent-color)[A Quantum ESPRESSO Recipe for $Z_2$ Invariant of 2D Topological Material 1T'-WTe#sub[2]]
  #v(1em)
  #text(22pt)[*Shahriar Pollob*]
  #v(0.2em)
  #text(18pt, style: "italic")[Supervised by M. Shahnoor Rahman]
  #v(2em)
  #line(length: 60%, stroke: 1pt + text-color)
  #v(0.5em)
  #text(18pt)[*ICAP 2025* | SUST] \
  #text(16pt, fill: text-color.lighten(30%))[International Conference on Advances in Physics]
]
#pagebreak()

// --- SLIDE 2: MOTIVATION & CONCEPT ---
#slide(title: "Motivation: The Reproducibility Gap")[
  *The Problem:* Obtaining topological invariants ($Z_2$) from standard DFT output is non-trivial and often relies on opaque, black-box tools.

  *Our Goal:* Provide a clear, open-source *"Recipe"* using Quantum ESPRESSO.

  #grid(
    columns: (1fr, 1fr),
    gutter: 20pt,
    [
      *Target Material: 1T'-WTe#sub[2]*
      - *Phase:* Distorted 1T structure (Peierls Instability).
      - *Mechanism:* SOC-driven Band Inversion ($d-p$ orbitals).
      - *Result:* Quantum Spin Hall (QSH) Insulator.
    ],
    align(center)[
      #image("figures/Fig_Structure_Views_V2.png", width: 80%)
      #text(14pt)[1T'-WTe#sub[2] Crystal Structure]
    ]
  )
]

// --- SLIDE 3: THE RECIPE (WORKFLOW) ---
#slide(title: "The Workflow: DFT to Topology")[
  We developed a minimally-interfaced pipeline to generate "Topology-Ready" data.

  #align(center)[
    #image("figures/Fig_Workflow.png", width: 85%)
  ]
  
  *Key Ingredients:*
  - *QE (pw.x):* Fully Relativistic PBE+SOC ($12 times 6 times 1$ k-mesh).
  - *Wannier90:* Spinor Projections ($p$-Te, $d$-W) + Disentanglement.
]

// --- SLIDE 4: ELECTRONIC STRUCTURE (DFT) ---
#slide(title: "Step 1: Relativistic Electronic Structure")[
  The foundation of the recipe is the accurate capture of the Spin-Orbit Coupling (SOC) effects.

  #grid(
    columns: (1fr, 1fr),
    gutter: 10pt,
    align(center)[
      #image("figures/Fig1_BandStructure_Final.png", height: 70%)
      #text(16pt)[*Band Structure:* SOC opens the direct gap at $Gamma$.]
    ],
    align(center)[
      #image("figures/Fig_PDOS_Inversion.png", height: 70%)
      #text(16pt)[*PDOS:* Orbital inversion confirm $d-p$ mixing.]
    ]
  )
]

// --- SLIDE 5: WANNIER QUALITY CONTROL ---
#slide(title: "Step 2: Wannierization Quality")[
  *Critique:* Topological claims are invalid if the Tight-Binding model is poor.
  *Validation:* We ensure strict convergence of the Wannier spreads.

  #grid(
    columns: (1fr, 1fr),
    gutter: 20pt,
    align(center)[
      #image("figures/Fig_Credibility_Spreads.png", height: 60%)
      #v(0.5em)
      *Convergence* \
      (Total Spread $< 30 Å^2$)
    ],
    align(center)[
      #image("figures/validation_dft_vs_wannier.png", height: 60%)
      #v(0.5em)
      *Accuracy* \
      (Overlay error $< 5$ meV)
    ]
  )
]

// --- SLIDE 6: TOPOLOGICAL DIAGNOSTICS (PIVOT) ---
#slide(title: "Step 3: Topological Diagnostics")[
  From the Wannier Hamiltonian, we diagnose the $Z_2$ invariant via the *Bulk-Boundary Correspondence*.
  
  #grid(
    columns: (1.5fr, 1fr),
    gutter: 20pt,
    align(center)[
      #image("figures/Fig_Ribbon_EdgeStates.png", width: 90%)
    ],
    align(horizon)[
      *Ribbon Calculation:*
      - We construct a 30-unit-cell slab.
      - *Result:* Helical Edge States (Red) traverse the bulk gap.
      - *Counting Rule:* Odd number of crossings $arrow Z_2 = 1$.
      
      This serves as a direct visualization of the Wilson Loop winding.
    ]
  )
]

// --- SLIDE 7: SPIN HALL CONDUCTIVITY ---
#slide(title: "Complementary Proof: SHC")[
  We further verify the topological phase by calculating the *Spin Hall Conductivity* (Kubo Formula).

  #grid(
    columns: (1.2fr, 1fr),
    gutter: 20pt,
    align(center)[
      #image("figures/Fig2_SHC_Final.png", width: 100%)
    ],
    align(horizon)[
      *Quantized Response:*
      - Plateau at $sigma_("xy") approx 2 e^2 / h$.
      - Robust against chemical potential shifts.
      - Confirms the QSH nature of the gap.
    ]
  )
]

// --- SLIDE 8: CONCLUSION & RESOURCES ---
#slide(title: "Takeaways & Resources")[
  - *Summary:*
    1.  Established a reproducible *Quantum ESPRESSO Recipe* for 1T'-WTe#sub[2].
    2.  Verified $Z_2=1$ via Edge States and SHC.
    3.  Demonstrated robust Wannierization ($< 30 Å^2$ spread).

  - *Open Science:*
    - The complete "Recipe" (Scripts, Inputs, Data) is available on GitHub.
  
  #align(center)[
    #v(1em)
    #image("figures/Fig_Repo_QR.png", width: 20%)
    #v(0.5em)
    #text(16pt)[github.com/shahpoll/Quantum-ESPRESSO-WTe2-Topology]
  ]
]
