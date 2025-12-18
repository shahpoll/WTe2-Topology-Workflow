// --- THEME CONFIGURATION ---
// Dark "Scientific Narrative" Aesthetic
#let bg-color = rgb("#1e1e2e") 
#let text-color = rgb("#cdd6f4")
#let accent-color = rgb("#f38ba8") // Red/Pink
#let secondary-color = rgb("#89b4fa") // Blue
#let card-bg = rgb("#313244")

#set page(
  paper: "presentation-16-9",
  fill: bg-color,
  margin: (x: 1.0cm, y: 1.0cm),
  numbering: "1"
)
#set text(
  font: "Linux Libertine",
  size: 20pt,
  fill: text-color
)

// Apply math color
#show math.equation: set text(fill: secondary-color)

// --- CUSTOM FUNCTIONS ---
// Assertive Slide Title
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

// Insight Card
#let card(body) = {
  block(
    fill: card-bg,
    stroke: (left: 5pt + accent-color),
    inset: 20pt,
    outset: 0pt,
    radius: 5pt,
    width: 100%,
    body
  )
}

// --- SLIDE 1: TITLE ---
#align(center + horizon)[
  #text(28pt, weight: "bold", fill: accent-color)[A Quantum ESPRESSO Recipe for $Z_2$ Invariant of 2D Topological Material 1T#super[#sym.prime]-WTe#sub[2]]
  #v(1em)
  
  // Authors
  #text(20pt)[
    Shahriar Pollob#super[1, \*], 
    Apu Das#super[2], 
    Mohammad Dilwar Ali Alvee#super[3], 
    M. Shahnoor Rahman#super[4]
  ]
  
  #v(1em)
  
  // Affiliations
  #text(15pt, style: "italic", fill: text-color.lighten(20%))[
    #super[1] Department of Physics, Shahjalal University of Science and Technology, Sylhet-3114, Bangladesh \
    #super[2] Department of Theoretical Physics, University of Dhaka, Dhaka-1000, Bangladesh \
    #super[3] Department of Materials Science & Engineering, Khulna University of Engineering & Technology, Khulna-9203, Bangladesh \
    #super[4] Department of Physics, University of Miami, Coral Gables, Florida 33124, USA \ 
    #super[\*] Presenter 
  ]

  #v(0.8em)
  #line(length: 60%, stroke: 1pt + text-color)
  #v(0.5em)
  #text(20pt)[*ICAP 2025* | SUST] \
  #text(16pt, fill: text-color.lighten(30%))[International Conference on Advances in Physics]
]
#pagebreak()

// --- SLIDE 2: MOTIVATION ---
#slide(title: "Motivation: The Quest for Dissipationless Electronics")[
  #align(center + horizon)[
    #stack(dir: ttb, spacing: 20pt,
      card[
        *The Bottleneck:* \
        Modern electronics suffer from Joule heating and backscattering limits.
      ],
      card[
        *The Solution:* \
        Topological Insulators (TIs) offer dissipationless edge transport protected by Time-Reversal Symmetry.
      ],
      card[
        *The Challenge:* \
        Obtaining the topological invariant ($Z_2$) from First-Principles is often a "Black Box."
      ]
    )
  ]
]

// --- SLIDE 3: 1T PHASE (IDEAL) ---
#slide(title: [Crystal Structure: The Ideal $1T$ Phase])[
  #grid(
    columns: (1.2fr, 1fr),
    gutter: 1em,
    [
      #align(center + horizon)[
        #image("figures/Fig_Structure_3D_1T.png", width: auto, height: 10cm)
      ]
    ],
    [
      #card[
        *The "Parent" Structure:* \
        - *Symmetry:* Perfect Octahedral Coordination.
        - *Lattice:* Hexagonal / Triangular W Lattice.
        
        *Why it fails:*
        - *Unstable:* High energy state.
        - *Metallic:* No band gap.
        - *Not Topological:* Trivial band structure.
      ]
    ]
  )
]

// slide 4: 1T' phase (distorted) ---
#slide(title: [Crystal Structure: The Distorted $1T#super[#sym.prime]$ Phase])[
  #grid(
    columns: (1.2fr, 1fr),
    gutter: 1em,
    [
      #align(center + horizon)[
        #image("figures/Fig_Structure_3D_Presentation.png", width: auto, height: 10cm)
      ]
    ],
    [
      #card[
        *The "Real" Structure:* \
        - *Symmetry:* Distorted (Peierls Instability).
        - *Action:* W atoms dimerize along one axis.
        
        *The Magic:*
        - *Stable:* Energetically favorable.
        - *Insulating:* Gap opens ($E_g > 0$).
        - *Topological:* Inverted Band Order ($Z_2=1$).
      ]
    ]
  )
]

// --- SLIDE 5: PHASE TRANSITION SCHEMATIC ---
#slide(title: "Phase Transition Mechanism")[
   #align(center + horizon)[
     #image("figures/Fig_Structure_Views.png", width: auto, height: 10cm)
   ]
]

// --- SLIDE 6: ELECTRONIC STRUCTURE (BANDS) ---
#slide(title: "Electronic Structure: Band Inversion")[
  #grid(
    columns: (1.2fr, 1fr),
    gutter: 1em,
    [
      #align(center + horizon)[
        #image("figures/Fig_Bands_Presentation.png", width: auto, height: 10cm)
      ]
    ],
    [
      #card[
        *Key Features:* \
        - *Band Inversion:* $p$-orbital bands swap parity near $Gamma$.
        - *Spin-Orbit Coupling:* Essential for opening the gap ($E_g approx 50$ meV).
        - *Direct Gap:* Located at $Q$ point (monolayer feature).
      ]
    ]
  )
]

// --- SLIDE 7: SPIN TEXTURE ---
#slide(title: "Spin Texture & Berry Curvature")[
    #grid(
    columns: (1fr, 1fr),
    gutter: 1em,
    [
      #align(center + horizon)[
        #image("figures/Fig2_SHC_Final.png", width: auto, height: 9.5cm)
      ]
    ],
    [
       #card[
        *Spin-Momentum Locking:* \
        - Spins are locked to momentum $k$.
        - Signatures of topological surface states.
        - *Result:* Suppression of backscattering.
      ]
    ]
  )
]

// --- SLIDE 8: EDGE STATES (THE EVIDENCE) ---
#slide(title: "The Definitive Evidence: Edge States")[
  #grid(
    columns: (1.5fr, 1fr),
    gutter: 1em,
    [
      #align(center + horizon)[
        #image("figures/Fig_Ribbon_EdgeStates.png", width: auto, height: 10cm)
      ]
    ],
    [
      #card[
        *Topological Protection:* \
        - *Gapless States:* Crossing the bulk gap.
        - *Conducting Channels:* Located physically at the edges.
        - *Robustness:* Immune to non-magnetic disorder.
      ]
    ]
  )
]


// --- SLIDE 3: MECHANISM ---
#slide(title: "The Mechanism: SOC-Driven Band Inversion")[
  #grid(
    columns: (1fr, 1fr),
    gutter: 30pt,
    align(center)[
       #image("figures/Fig_PDOS_Inversion.png", width: 95%) 
    ],
    [
      #card[
        *Orbital Physics:*
        1. *Crystal Field:* Splits W-$d$ orbitals.
        2. *Spin-Orbit Coupling (SOC):* The heavy Tungsten core drives a relativistic energy shift.
        
        *The Inversion:*
        The W-$d$ and Te-$p$ bands *exchange parity eigenvalues* near the Fermi level. This crossing opens a non-trivial gap.
      ]
    ]
  )
]

// --- SLIDE 4: RECIPE ---
#slide(title: "The Recipe: A Reproducible QE Pipeline")[
  Our pipeline automates the extraction of "Topology-Ready" Hamiltonians.
  
  #grid(
    columns: (2fr, 1fr),
    gutter: 30pt,
    align(center)[
      #image("figures/Fig_Workflow.png", width: 100%)
    ],
    [
       #card[
         *Key Ingredients:*
         - *Engine:* Quantum ESPRESSO (`pw.x`) v7.4.1
         - *Pseudopotentials:* `pslibrary` v1.0.0 (PAW, Fully Relativistic PBE)
         - *Wannier90:* Spinor Projections ($p$-Te, $d$-W) + Disentanglement
         
         *Goal:* \
         Generate an accurate Tight-Binding model for Berry Curvature integration.
       ]
    ]
  )
]

// --- SLIDE 5: GEOMETRIC FRAMEWORK (BZ) ---
#slide(title: "The Arena: Reciprocal Space Geometry")[
  To capture the inversion, one must traverse specific high-symmetry points.
  
  #grid(
    columns: (1.2fr, 1fr),
    gutter: 30pt,
    align(center)[
       #image("figures/Fig_BZ_Schematic.png", width: 100%)
    ],
    [
      #card[
        *The Path:* \
        $bold(Gamma) arrow bold(X) arrow bold(M) arrow bold(Gamma) arrow bold(Y)$
        
        *Significance:*
        - The fundamental gap opens at $bold(Gamma)$.
        - The $bold(M) arrow bold(Gamma)$ diagonal is critical for identifying background nodal lines.
        - Rectangular BZ reflects the 1T#super[#sym.prime] anisotropy.
      ]
    ]
  )
]

// --- SLIDE 6: FINGERPRINT (BAND STRUCTURE) ---
#slide(title: "The Fingerprint: Relativistic Band Inversion")[
  #grid(
    columns: (1.3fr, 1fr),
    gutter: 20pt,
    align(center)[
      #image("figures/Fig_Bands_Presentation.png", width: 100%)
      #text(16pt)[Full Relativistic Band Structure]
    ],
    [
      #card[
        *Global Profile:* \
        Semimetallic overlap observed (typical for PBE), *BUT*...
        
        *The Topological Signal:*
        A clear, direct gap opens at $Gamma$.
      ]
      #v(1em)
      #figure(image("figures/Fig_PDOS_Inversion.png", width: 100%), caption: [Zoom at $Gamma$: Parity Exchange])
    ]
  )
]

// --- SLIDE 7: COMPLICATION ---
#slide(title: "A Complication: The Semimetallic Ground State")[
  #grid(
    columns: (1fr, 1fr),
    gutter: 30pt,
    align(center)[
      #image("figures/Fig1_BandStructure_Final.png", width: 90%)
      #place(center + bottom, dy: -20%)[
          #block(fill: rgb("#f38ba880"), inset: 10pt, radius: 5pt)[*Indirect Overlap*]
      ]
    ],
    [
      #card[
        *The Observation:* \
        The Conduction Band Minimum (CBM) dips below the Valence Band Maximum (VBM) at different k-points ($Q$ vs $Gamma$).
        
        *The Explanation:* \
        PBE functionals notoriously underestimate gaps.
        
        *The Crucial Insight:* \
        Topology is defined by the *Inverted Direct Gap*. As long as the direct gap at $Gamma$ is non-zero and inverted, the $Z_2$ invariant is robust.
      ]
    ]
  )
]

// --- SLIDE 8: SHC ---
#slide(title: "Definitive Evidence I: Quantized Transport")[
  The Spin Hall Conductivity (SHC) provides a measurable order parameter.
  
  #grid(
    columns: (1.5fr, 1fr),
    gutter: 30pt,
    align(center)[
      #image("figures/Fig2_SHC_Final.png", width: 100%)
    ],
    [
      #card[
        *The Observable:* \
        $sigma_("xy")^("spin")$ calculated via Kubo-Greenwood formula.
        
        *The Result:* \
        A quantized plateau exists at exactly: 
        $ 2 e^2 / h $
        
        *Implication:* \
        This quantization is the hallmark of the Quantum Spin Hall (QSH) state, protected against non-magnetic perturbations.
      ]
    ]
  )
]

// --- SLIDE 9: RIBBON ---
#slide(title: "Definitive Evidence II: Visualizing Edge Highways")[
  Bulk-Boundary Correspondence guarantees conductive states at the interface.
  
  #grid(
    columns: (1.2fr, 1fr),
    gutter: 30pt,
    align(center)[
      #image("figures/Fig_Ribbon_EdgeStates.png", width: 100%)
    ],
    [
      #card[
        *Calculation:* \
        Wannier Hamiltonian projected onto a 30-unit-cell finite slab.
        
        *Observation:* \
        Helical edge states (Red) traverse the bulk gap, connecting valence and conduction bands.
        
        *Verdict:* \
        Odd number of crossings $arrow Z_2 = 1$.
      ]
    ]
  )
]

// --- SLIDE 10: EFFICIENCY ---
#slide(title: "The Efficiency: Accelerated Discovery")[
  Topological workflows are computationally expensive. We benchmarked the feasibility.
  
  #grid(
    columns: (1fr, 1fr),
    gutter: 30pt,
    align(center)[
       #image("figures/Fig_Feasibility_Time.png", width: 90%)
    ],
    [
      #card[
        *The Speedup:* \
        GPU Acceleration reduces iteration time from *4 hours* to *20 minutes* (12x).
        
        *Why it Matters:* \
        Allows for rapid convergence testing ($k$-mesh density, Wannier windows) essential for high-fidelity topological invariants.
      ]
    ]
  )
]

// --- SLIDE 11: VERDICT ---
#slide(title: "The Verdict: Unambiguous QSH Insulator")[
  Our "Recipe" successfully characterizes 1T#super[#sym.prime]-WTe#sub[2].
  
  #grid(
    columns: (1fr, 1fr),
    gutter: 20pt,
    [
      #card[
        *Summary of Evidences:*
        1. *Orbital:* $d-p$ Band Inversion confirmed.
        2. *Topology:* $Z_2=1$ via Edge States and SHC.
        3. *Robustness:* Wannier spreads $< 30 Å^2$.
        
        *Final Conclusion:* \
        1T'-WTe#sub[2] is a robust Quantum Spin Hall Insulator suitable for room-temperature spintronics.
      ]
    ],
    align(center + horizon)[
      #image("figures/Fig_Repo_QR_Branded.png", width: 60%)
      #v(1em)
      *Code & Data:* \
      #text(16pt)[github.com/shahpoll/Quantum-ESPRESSO-WTe2-Topology]
      #v(0.5em)
      *Release:* \
      #text(16pt)[`v1.0-ICAP2025` (Verified Artifact)]
    ]
  )
]
