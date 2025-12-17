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
    
    colors = ['#2c3e50' if s == 'W' else '#f39c12' for s in species]
    sizes = [400 if s == 'W' else 200 for s in species] # 3D scatter requires diff scaling?
    
    ax.scatter(xs, ys, zs, c=colors, s=sizes, edgecolors='black', depthshade=True, alpha=1.0)
    
    # 3. Draw Unit Cell Box (In-Plane Only for Monolayer)
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
    
    # Aspect Ratio - CRITICAL for removing whitespace
    # We want X and Y to be proportional, and Z to be squashed
    ax.set_box_aspect((np.ptp(xs), np.ptp(ys), 0.3 * np.ptp(xs))) 
    
    # Labels
    ax.set_xlabel(r"$x$ ($\AA$)", labelpad=10)
    ax.set_ylabel(r"$y$ ($\AA$)", labelpad=10)
    ax.set_zlabel(r"$z$ ($\AA$)", labelpad=15) # Increased padding to prevent cutoff
    ax.set_title("1T'-WTe2 Crystal Structure", pad=0)
    
    # Limits
    ax.set_xlim(min(xs), max(xs))
    ax.set_ylim(min(ys), max(ys))
    ax.set_zlim(z_mean - 2, z_mean + 2)
    
    # Turn off Z ticks? They don't mean much for a floating monolayer
    ax.set_zticks([])
    
    # Save
    out_dir = os.path.dirname(os.path.abspath(__file__)) + "/../figures"
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    plt.savefig(f"{out_dir}/Fig_Structure_3D_Presentation.png", dpi=300, bbox_inches='tight')
    print(f"Saved {out_dir}/Fig_Structure_3D_Presentation.png")

if __name__ == "__main__":
    plot_3d_structure()
