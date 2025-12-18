import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from itertools import product
import os
import sys

# --- PROJECTOR SETTINGS ---
params = {
    'figure.figsize': (12, 10),
    'font.family': 'sans-serif',
    'font.weight': 'bold',
    'axes.labelweight': 'bold',
    'font.size': 18,
}
plt.rcParams.update(params)

BOHR_TO_ANG = 0.529177

def parse_qe_input(filename):
    atoms = []
    cell = []
    if not os.path.exists(filename):
        # Fallback paths
        if os.path.exists(f"../{filename}"): filename = f"../{filename}"
        elif os.path.exists(f"repo/{filename}"): filename = f"repo/{filename}"
        else: return None, None
        
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    # Parse Cell
    for i, line in enumerate(lines):
        if "CELL_PARAMETERS" in line:
            scale = BOHR_TO_ANG if "bohr" in line.lower() else 1.0
            v1 = np.array([float(x) for x in lines[i+1].split()]) * scale
            v2 = np.array([float(x) for x in lines[i+2].split()]) * scale
            v3 = np.array([float(x) for x in lines[i+3].split()]) * scale
            cell = np.array([v1, v2, v3])
            break
            
    # Parse Atoms
    in_atoms = False
    atom_scale = 1.0
    for line in lines:
        if "ATOMIC_POSITIONS" in line:
            in_atoms = True
            if "bohr" in line.lower(): atom_scale = BOHR_TO_ANG
            elif "crystal" in line.lower(): atom_scale = 'crystal'
            continue
        if in_atoms:
            if line.strip() == "" or "K_POINTS" in line: break
            parts = line.split()
            if len(parts) >= 4:
                species = parts[0]
                coords = np.array([float(x) for x in parts[1:4]])
                if atom_scale == 'crystal':
                    cart = coords[0]*cell[0] + coords[1]*cell[1] + coords[2]*cell[2]
                    atoms.append({'s': species, 'pos': cart})
                else:
                    atoms.append({'s': species, 'pos': coords * atom_scale})
                    
    return cell, atoms

def get_supercell(cell, atoms, dim=(2,2,1)):
    # Expand unit cell to supercell
    super_atoms = []
    nx, ny, nz = dim
    
    # Range centered around 0 to look nice? Or just positive.
    # Let's do 0 to N
    for i, j, k in product(range(nx), range(ny), range(nz)):
        shift = i*cell[0] + j*cell[1] + k*cell[2]
        for atom in atoms:
            pos = atom['pos'] + shift
            super_atoms.append({'s': atom['s'], 'pos': pos})
            
    return super_atoms

def draw_bonds(ax, atoms, cutoff=3.2):
    # Brute force distance optimization
    pos = np.array([a['pos'] for a in atoms])
    n = len(atoms)
    
    # Store plotted bonds to avoid dupes drawn twice? 
    # Matplotlib draws painter's algo, so drawing twice is fine/inefficient but okay.
    
    for i in range(n):
        for j in range(i+1, n):
            p1 = pos[i]
            p2 = pos[j]
            d = np.linalg.norm(p1 - p2)
            if d < cutoff:
                # Bond Logic:
                # W-Te ~ 2.8 A
                # W-W (zigzag) ~ 2.8 A
                # Te-Te typically longer > 3.5
                
                # Check species
                s1, s2 = atoms[i]['s'], atoms[j]['s']
                
                # Style based on bond type?
                lw = 2
                color = 'gray'
                if s1 == 'W' and s2 == 'W':
                    color = '#2c3e50' # Dark Blue bond
                    lw = 3
                elif (s1 == 'W' and s2 == 'Te') or (s1 == 'Te' and s2 == 'W'):
                    color = 'gray'
                    lw = 2
                else:
                    continue # Skip Te-Te if any
                
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 
                        color=color, linewidth=lw, alpha=0.6)

def plot_3d_structure():
    cell, unit_atoms = parse_qe_input('wte2.scf.in')
    if not cell.any():
        print("Could not parse input.")
        sys.exit(1)
        
    # Create Supercell for connectivity visualization
    # 2x2x1 is standard
    atoms = get_supercell(cell, unit_atoms, dim=(2,2,1))
    
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # 1. Draw Bonds FIRST (so atoms sit on top)
    draw_bonds(ax, atoms, cutoff=3.0) 
    
    # 2. Draw Atoms
    xs = [a['pos'][0] for a in atoms]
    ys = [a['pos'][1] for a in atoms]
    zs = [a['pos'][2] for a in atoms]
    species = [a['s'] for a in atoms]

    # Identify Central Cell Atoms vs Supercell Ghosts
    # "Central" if they are the original atoms (before expansion loop in get_supercell logic)
    # Actually get_supercell returns a flat list.
    # Logic: The first N atoms are usually the unit cell? No, get_supercell iterates lattice.
    # Let's filter by position? If inside unit cell?
    # Simple Heuristic: If x,y is roughly within 0..a and 0..b?
    # Better: Identify indices.
    
    # Let's rewrite get_supercell to track if it's the central cell (i=0, j=0, k=0)
    # But existing get_supercell is: for i,j,k...
    # We can assume central cell is somewhere in the middle of 2x2?
    # The user wants "one unit cell bold".
    # Let's pick the cell at index (0,0) or (1,0)?
    # Since visual box is 2x2, let's pick cell (0,0) as Bold.
    
    colors = []
    alphas = []
    edgecolors = []
    
    # Re-calculate which cell each atom belongs to
    n_unit = len(unit_atoms)
    
    for idx, atom in enumerate(atoms):
        species_s = atom['s'] # Renamed to avoid conflict with outer 'species' list
        # Determine if this atom belongs to the "Primary" Unit Cell
        # We constructed it by looping i,j,k.
        # idx % n_unit gives index in unit cell.
        # idx // n_unit gives cell index.
        # Loop order: i(0..nx), j(0..ny), k(0..nz).
        # We want i=0, j=0, k=0 (First block) to be bold?
        # Or maybe the one in the middle?
        # Let's make the FIRST cell bold for clarity.
        
        is_primary = (idx < n_unit) 
        
        if species_s == 'W':
            base_color = '#2c3e50'
        else:
            base_color = '#f39c12'
            
        if is_primary:
            colors.append(base_color) # Bold
            alphas.append(1.0)
            edgecolors.append('black')
        else:
            # Ghost / Faded
            # Use distinct light color or just alpha?
            # User said: "make it a bit light colored"
            if species_s == 'W':
                colors.append('#bdc3c7') # Light Gray/Blue
            else:
                colors.append('#fcd088') # Light Orange
            alphas.append(0.8) # Slight fade
            edgecolors.append('gray')

    sizes = [400 if s == 'W' else 200 for s in species]
    
    ax.scatter(xs, ys, zs, c=colors, s=sizes, edgecolors=edgecolors, depthshade=False, alpha=alphas)
    
    # Calculate Centroid of Primary Cell (is_primary logic)
    # n_unit is number of atoms in unit cell.
    n_unit = len(unit_atoms)
    
    # Primary atoms are the first n_unit atoms in the 'atoms' list
    primary_pos = [a['pos'] for a in atoms[:n_unit]]
    
    # Need to check if logic inside plot_3d_structure modified positions?
    # No, plot_3d_structure uses 'atoms' list directly and extracts xs, ys, zs.
    # But wait, did I modify 'xs', 'ys', 'zs' variable in previous script versions?
    # NO, looking at the code, it extracts:
    # xs = [a['pos'][0] for a in atoms]
    # And then scatter uses xs.
    # So 'atoms' list has the data.
    
    primary_pos = np.array(primary_pos)
    primary_centroid = np.mean(primary_pos, axis=0)
    
    print("DEBUG_PRIMARY_CENTROID:", primary_centroid)

    # Unit Cell Box (In-Plane Only for Monolayer)
    # Drawing full vacuum box creates huge whitespace. 
    # We project the box to the mean Z height of atoms.
    z_mean = np.mean(zs)
    
    # Vectors (Using only a and b)
    origin_shift = np.array([0., 0., z_mean]) # Center box on atoms
    v1, v2 = cell[0], cell[1]
    
    # Draw simple 2D parallelogram at z_mean
    # Vertices: 0, v1, v1+v2, v2, 0
    box_points = [
        origin_shift,
        origin_shift + v1,
        origin_shift + v1 + v2,
        origin_shift + v2,
        origin_shift
    ]
    
    bx = [p[0] for p in box_points]
    by = [p[1] for p in box_points]
    bz = [p[2] for p in box_points]
    
    ax.plot(bx, by, bz, color='red', linestyle='--', alpha=0.9, linewidth=2.5, label='Unit Cell')

    # 4. Camera & Aesthetics
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.grid(False)
    
    # Isometric View
    ax.view_init(elev=30, azim=-60)
    
    # Aspect Ratio - FIXED for Flipbook Alignment
    # X range = 10 (-2 to 8), Y range = 10 (-4 to 6) -> Ratio 1:1
    # Z range = 6 (-3 to 3) -> Ratio 0.6 relative to X?
    # Let's set strictly.
    ax.set_box_aspect((10, 10, 2)) 
    
    # Labels
    ax.set_xlabel(r"$x$ ($\AA$)", labelpad=10)
    ax.set_ylabel(r"$y$ ($\AA$)", labelpad=10)
    ax.set_zlabel(r"$z$ ($\AA$)", labelpad=25) # Increased padding to fix distortion/clipping
    ax.set_title(r"1T'-WTe$_2$ (Distorted)", pad=0, fontsize=24) 
    
    # Limits - TIGHTENED to remove whitespace
    # Atoms roughly 0 to 7 in X/Y.
    # Center around (3.5, 3.5).
    # Range of 8 should be enough? (0 to 8)
    # Limits - DYNAMIC to strict bounding box + padding
    x_range = np.max(xs) - np.min(xs)
    y_range = np.max(ys) - np.min(ys)
    padding = 0.5
    
    # Shave off left whitespace by reducing min padding
    ax.set_xlim(np.min(xs) - 0.1, np.max(xs) + padding)
    ax.set_ylim(np.min(ys) - padding, np.max(ys) + padding)
    ax.set_zlim(np.mean(zs) - 3, np.mean(zs) + 3)
    
    # Aspect Ratio - Match the Data Ratio exactly
    # Z range is fixed at 6 (-3 to 3 relative)
    ax.set_box_aspect((x_range + 2*padding, y_range + 2*padding, 6.0))
    
    # Labels
    ax.set_xlabel(r"$x$ ($\AA$)", labelpad=10)
    ax.set_ylabel(r"$y$ ($\AA$)", labelpad=10)
    ax.set_zlabel(r"$z$ ($\AA$)", labelpad=12) # Reduced padding to bring closer
    
    # Title - Lowered
    # 'y' controls vertical position (1.0 is top of box, >1 is above).
    # Default is often >1. Let's try 0.95 or 1.0 strictly.
    ax.set_title(r"1T'-WTe$_2$ (Distorted)", pad=-20, fontsize=24, y=1.02) 
    
    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='W',
               markerfacecolor='#2c3e50', markersize=15, markeredgecolor='black'),
        Line2D([0], [0], marker='o', color='w', label='Te',
               markerfacecolor='#f39c12', markersize=12, markeredgecolor='black')
    ]
    ax.legend(handles=legend_elements, loc='upper left', frameon=False, fontsize=14)

    # Turn ON Z ticks
    
    # Save
    out_dir = os.path.dirname(os.path.abspath(__file__)) + "/../figures"
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    # Use tighter bbox padding
    plt.savefig(f"{out_dir}/Fig_Structure_3D_Presentation.png", dpi=300, bbox_inches='tight', pad_inches=0.02)
    print(f"Saved {out_dir}/Fig_Structure_3D_Presentation.png")
    
    print("DEBUG_LIMITS_X:", ax.get_xlim())
    print("DEBUG_LIMITS_Y:", ax.get_ylim())
    print("DEBUG_LIMITS_Z:", ax.get_zlim())
    print("DEBUG_ASPECT:", ax.get_box_aspect())
    
    # Also print the axis title and labelpad settings to confirm
    print("DEBUG_TITLE_Y:", ax.title.get_position()[1])

if __name__ == "__main__":
    plot_3d_structure()
