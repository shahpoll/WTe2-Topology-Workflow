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
  numbering: none
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
        *The "Parent" Phase:* \
        - *Geometry:* High Symmetry ($C_(3v)$).
        - *Feature:* Uniform W triangular lattice.
        
        *The Physics:*
        - *Stability:* Unstable (Peierls active).
        - *Band Order:* Normal (Trivial).
        - *Topology:* $Z_2 = 0$ (Ordinary Metal).
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
        *The "Real" Phase:* \
        - *Geometry:* Low Symmetry ($C_(2h)$).
        - *Feature:* W atoms form zig-zag chains.
        
        *The Physics:*
        - *Stability:* Ground State (Relaxed).
        - *Band Order:* Inverted (Topological).
        - *Topology:* $Z_2 = 1$ (QSH Insulator).
      ]
    ]
  )
]

// --- SLIDE 5: PHASE TRANSITION MECHANISM ---
#slide(title: "The Bridge: From Instability to Topology")[
  #align(center + horizon)[
    #stack(dir: ttb, spacing: 8pt,
      block(
        fill: card-bg, stroke: (left: 5pt + accent-color), inset: 10pt, radius: 5pt, width: 100%,
        text(20pt)[
          *The Driving Force: Peierls Instability* \
          The metallic 1T phase is energetically expensive. The system lowers its total energy by spontaneously distorting the lattice (dimerization).
        ]
      ),
      block(
        fill: card-bg, stroke: (left: 5pt + accent-color), inset: 10pt, radius: 5pt, width: 100%,
        text(20pt)[
          *The Structural Response: Symmetry Breaking* \
           $C_(3v) arrow C_(2h)$ \
          Tungsten (W) atoms pair up to form zigzag chains. This lowers the symmetry and opens a fundamental band gap.
        ]
      ),
      block(
        fill: card-bg, stroke: (left: 5pt + accent-color), inset: 10pt, radius: 5pt, width: 100%,
        text(20pt)[
          *The Topological Consequence* \
          This distortion is not trivial—it induces a *Band Inversion* between $d$ and $p$ orbitals, turning the material into a QSH Insulator ($Z_2=1$).
        ]
      )
    )
  ]
]

// --- SLIDE 6: SIMULATION SETUP ---
#slide(title: "Simulation Setup: From Structure to Input")[
  #grid(
    columns: (1.6fr, 1fr),
    gutter: 1em,
    [
      #card[
        *The Foundation:* \
        - *Structure:* Optimized via `vc-relax` (BFGS).
        - *Vacuum:* $> 15 Å$ isolation for monolayer physics.
        
        *The Engine (QE v7.4.1):*
        - *Functional:* PBE + Spin-Orbit Coupling (SOC).
        - *Pseudos:* Fully Relativistic PAW (`pslibrary`).
        
        *Numerical Precision:*
        - *Kinetic Cutoff:* 60 Ry (Wvfn) / 720 Ry (Rho).
        - *K-Mesh:* $12 times 6 times 1$ (Monkhorst-Pack).
        - *Convergence:* $10^(-8)$ Ry (SCF).
      ]
    ],
    [
      #align(center + horizon)[
        #block(fill: card-bg, inset: 10pt, radius: 5pt)[
          #text(16pt)[
            ```fortran
            &SYSTEM
            ibrav=0, nat=6, ntyp=2,
            ecutwfc=60, ecutrho=720,
            lspinorb=.true.,
            noncolin=.true.,
            /
            ATOMIC_SPECIES
            W  183.84 W.rel...UPF
            Te 127.60 Te.rel...UPF
            K_POINTS (automatic)
            12 6 1 0 0 0
            ```
          ]
        ]
        #v(0.5em)
        *Real Input Snapshot*
      ]
    ]
  )
]

// --- SLIDE 6: RECIPE ---
#slide(title: "The Recipe: A Reproducible QE Pipeline")[
  Our pipeline automates the extraction of "Topology-Ready" Hamiltonians.
  
  #v(-2em) // Pull up to prevent page break
  #grid(
    columns: (2.5fr, 1fr), // Maximize figure space
    gutter: 20pt,
    align(center + horizon)[
      #image("figures/Fig_Workflow.png", width: 100%)
    ],
    [
       #card[
         #text(16pt)[
           *Key Ingredients:*
           - *Engine:* Quantum ESPRESSO.
           - *Pseudopotentials:* `pslibrary` (PAW, PBE).
           - *Wannier90:* Spinor Projections ($p$-Te, $d$-W) + Disentanglement.
           
           *Goal:* \
           Generate an accurate Tight-Binding model for Berry Curvature integration.
         ]
       ]
    ]
  )
]

// --- SLIDE 7: MECHANISM ---
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

// --- SLIDE 7: THE ARENA (BZ) ---
#slide(title: "The Arena: Reciprocal Space Geometry")[
  // To capture the topology, we must map the Real Space distortion into Reciprocal Space.
  
  #grid(
    columns: (1fr, 1.15fr),
    gutter: 20pt,
    align(center + horizon)[
       #image("figures/Fig_BZ_Schematic.png", width: 90%)
    ],
    [
      #card[
        #text(18pt)[
          *The Transformation:* \
          The $C_{2h}$ symmetry breaking (Slide 5) transforms the parent Hexagonal BZ into a *Rectangular BZ*.
          
          *The Path:* \
          $bold(Gamma) arrow bold(X) arrow bold(M) arrow bold(Gamma) arrow bold(Y)$
          
          *The Target:* \
          We must focus on the $bold(Gamma)$ point, where the band inversion corresponds to the "twisted" orbital character.
        ]
      ]
    ]
  )
]

// --- SLIDE 9: FINGERPRINT (BAND STRUCTURE) ---
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
        *The Effect of SOC:* \
        Spin-Orbit Coupling lifts the band degeneracy. The heavy Tungsten atoms drive a massive splitting.
        
        *The Topological Signal:*
        A fundamental *inverted gap* opens continuously along the $Gamma-X$ direction.
      ]
    ]
  )
]

// --- SLIDE 9: GLOBAL STRUCTURE ---
#slide(title: "Global Electronic Structure: The Semimetallic Reality")[
  #v(-1em)
  #grid(
    columns: (1.2fr, 1fr),
    gutter: 20pt,
    align(center + horizon)[
      // Simulating a "Zoomed Landscape" crop using Typst clipping
      #box(height: 180pt, width: 100%, clip: true)[
        #align(left + horizon)[
           // Focus on the Left side (Gamma -> X direction) where the overlap is
           #image("figures/Fig_Bands_Presentation.png", width: 220%)
        ]
      ]
      #place(center + bottom, dy: -20%)[
          #block(fill: rgb("#f38ba880"), inset: 5pt, radius: 5pt)[*Indirect Overlap (Zoomed at $Gamma-X$)*]
      ]
    ],
    [
      #card[
        #text(18pt)[
          *The Observation:* \
          CBM dips below VBM globally ($Q$ vs $Gamma$).
          
          *The Cause:* \
          Standard PBE underestimates gaps. This "Semimetallic" state is a known simulation feature of $1T'-"WTe"_2$.
          
          *Why Topology Survives:* \
          $Z_2$ depends on *Local Parity Exchange*. Size of the global gap is irrelevant as long as the direct gap at $Gamma$ is inverted.
        ]
      ]
    ]
  )
]

// --- SLIDE 11: SHC ---
#slide(title: "Definitive Evidence I: Quantized Transport")[
  #v(-1em)
  #grid(
    columns: (1.3fr, 1fr),
    gutter: 20pt,
    align(center + horizon)[
      #image("figures/Fig2_SHC_Final.png", width: 85%)
    ],
    [
      #card[
        #text(17pt)[
          *The Observable:* \
          Spin Hall Conductivity ($sigma_("xy")^("spin")$).
          
        *The Result:* \
        A robust quantized plateau (~50 meV width) exists at exactly: 
        $ 2 e^2 / h $
        
        *Implication:* \
        This quantization is the hallmark of the QSH state. The plateau confirms protection against non-magnetic disorder.
        ]
      ]
    ]
  )
]

// --- SLIDE 12: RIBBON ---
#slide(title: "Definitive Evidence II: Visualizing Edge Highways")[
  #v(-2em)
  #grid(
    columns: (1.2fr, 1fr),
    gutter: 20pt,
    // Column 1: The Figure (Zoomed & Colored)
    [
      #align(center + horizon)[ 
         #image("figures/Fig_Ribbon_EdgeStates.png", width: 85%)
      ]
    ],
    [
      #card[
        #text(17pt)[
          *Calculation:* \
          Wannier Hamiltonian (Finite Slab Projection).
          
          *Observation:* \
          Two distinct *Helical Edge States* traverse the bulk gap using opposite spin channels ($arrow.t k_x$ vs $arrow.b -k_x$).
          
          *The Connection:* \
          These are the "wires" that carry the quantized current seen in the previous slide ($2 e^2/h$).
        ]
      ]
    ]
  )
]

// --- SLIDE 13: EFFICIENCY ---
// --- SLIDE 13: EFFICIENCY ---
#slide(title: "The Efficiency: Accelerated Discovery")[
  #v(-1em)
  Topological workflows are computationally expensive. We benchmarked the feasibility.
  
  #grid(
    columns: (1fr, 1fr),
    gutter: 30pt,
    align(center + horizon)[
       #image("figures/Fig_Feasibility_Time.png", width: 85%)
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

// --- SLIDE 14: VERDICT ---
#slide(title: "The Verdict: Unambiguous QSH Insulator")[
  Our "Recipe" successfully characterizes 1T#super[#sym.prime]-WTe#sub[2].
  
  #v(-1em) // Move compaction here to avoid overlapping the header line
  #grid(
    columns: (1.1fr, 0.9fr), // Give text slightly more space
    gutter: 20pt,
    // Column 1: Text Summary (Centered Vertically)
    [
      #align(center + horizon)[
        #card[
          #text(17pt)[
            *Summary of Evidences:*
            1. *Orbital:* $d-p$ Band Inversion confirmed.
            2. *Topology:* $Z_2=1$ via Edge States and SHC.
            3. *Robustness:* Wannier spreads $< 30 Å^2$.
            
            *Final Conclusion:* \
            1T'-WTe#sub[2] is a robust Quantum Spin Hall Insulator suitable for room-temperature spintronics.
          ]
        ]
      ]
    ],
    align(center + horizon)[
      // Shift right column UP as requested to fix overflow
      #move(dy: -2em)[
        #image("figures/Fig_Repo_QR_Branded.png", width: 50%)
        #v(0.2em)
        *Code & Data:* \
        #text(15pt)[github.com/shahpoll/QE-WTe2-Topology]
        #v(0.1em)
        *Release:* \
        #text(15pt)[`v1.0-ICAP2025` (Verified Artifact)]
      ]
    ]
  )
]

// --- SLIDE 16: THANK YOU ---
#slide(title: none)[
  #align(center + horizon)[
    #text(40pt, weight: "bold", fill: accent-color)[Thank You!]
    #v(1em)
    #text(24pt, fill: text-color)[Questions & Discussion]
    #v(2em)
    #image("figures/Fig_Repo_QR_Branded.png", width: 25%)
    #v(0.5em)
    #text(16pt, fill: secondary-color)[github.com/shahpoll/QE-WTe2-Topology]
  ]
]
