import matplotlib.pyplot as plt
import numpy as np
import os
import sys

# --- PROJECTOR SETTINGS ---
# Large fonts, bold lines, high contrast
params = {
    'axes.labelsize': 22,
    'axes.titlesize': 26,
    'xtick.labelsize': 18,
    'ytick.labelsize': 18,
    'lines.linewidth': 3,
    'figure.figsize': (14, 6), # Wider for side-by-side
    'font.family': 'sans-serif',
    'font.weight': 'bold',
    'axes.labelweight': 'bold',
    'axes.titleweight': 'bold',
}
plt.rcParams.update(params)

# Conversion factor
BOHR_TO_ANG = 0.529177

def parse_qe_input(filename):
    # (Same parsing logic as before, robustified)
    atoms = []
    cell = []
    
    # Defaults
    pos_unit = 'alat'
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        sys.exit(1)
        
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    # 1. Parse Cell
    for i, line in enumerate(lines):
        if "CELL_PARAMETERS" in line:
            if "bohr" in line.lower():
                cell_scale = BOHR_TO_ANG
            elif "angstrom" in line.lower():
                cell_scale = 1.0
            else:
                cell_scale = 1.0 
            v1 = [float(x) for x in lines[i+1].split()]
            v2 = [float(x) for x in lines[i+2].split()]
            v3 = [float(x) for x in lines[i+3].split()]
            cell = np.array([v1, v2, v3]) * cell_scale
            break
            
    # 2. Parse Atoms
    in_atoms = False
    atom_scale = 1.0
    
    for line in lines:
        if "ATOMIC_POSITIONS" in line:
            in_atoms = True
            if "bohr" in line.lower():
                atom_scale = BOHR_TO_ANG
            elif "angstrom" in line.lower():
                atom_scale = 1.0
            elif "crystal" in line.lower():
                atom_scale = 'crystal'
            continue
            
        if in_atoms:
            if line.strip() == "" or "K_POINTS" in line:
                break
            parts = line.split()
            if len(parts) >= 4:
                species = parts[0]
                coords = np.array([float(parts[1]), float(parts[2]), float(parts[3])])
                
                if atom_scale == 'crystal':
                    cart_coords = coords[0]*cell[0] + coords[1]*cell[1] + coords[2]*cell[2]
                    atoms.append({'s': species, 'pos': cart_coords})
                else:
                    atoms.append({'s': species, 'pos': coords * atom_scale})
    return cell, atoms

# --- EXECUTION ---
# Path relative to script execution (usually repo root)
INPUT_FILE = 'repo/wte2.scf.in' 
# Fallback to current dir if running from repo/scripts/
if not os.path.exists(INPUT_FILE):
    INPUT_FILE = '../wte2.scf.in'
if not os.path.exists(INPUT_FILE):
    # Try absolute path based on user knowledge
    INPUT_FILE = '/home/pollob/qe_server_jarvis/wte2.scf.in'

try:
    cell, atoms = parse_qe_input(INPUT_FILE)
    print(f"Parsed Cell. a={np.linalg.norm(cell[0]):.2f}, b={np.linalg.norm(cell[1]):.2f}")
except Exception as e:
    print(f"Parsing Error: {e}")
    sys.exit(1)

fig = plt.figure()

# --- SUBPLOT 1: TOP VIEW (a-b plane) ---
ax1 = fig.add_subplot(1, 2, 1)

# Plot Primary Atoms
for atom in atoms:
    # W = Blue, Te = Gold
    # Make Markers HUGE for projector visibility
    color = '#1f77b4' if atom['s'] == 'W' else '#d62728' # Blue vs Red (high contrast)
    # Using specific hex for "Science" look: Gold (#E6B800) is standard for Te/S usually but Red pops better against white? 
    # Let's stick to standard: W (Blue/Grey), Te (Orange/Gold)
    color = '#2c3e50' if atom['s'] == 'W' else '#f39c12' # Dark Blue vs Orange
    
    size = 600 if atom['s'] == 'W' else 300 # HUGE markers
    zorder = 10 if atom['s'] == 'W' else 5
    
    x, y, z = atom['pos']
    ax1.scatter(x, y, c=color, s=size, edgecolors='black', linewidth=1.5, zorder=zorder)
    
    # 2x2 Supercell Phantom
    shifts = [[1,0,0], [0,1,0], [1,1,0], [-1,0,0], [0,-1,0]]
    for s in shifts:
        s_vec = s[0]*cell[0] + s[1]*cell[1] + s[2]*cell[2]
        new_pos = atom['pos'] + s_vec
        # Plot only if within a reasonable window
        if -2 < new_pos[0] < 10 and -2 < new_pos[1] < 10:
             ax1.scatter(new_pos[0], new_pos[1], c=color, s=size, edgecolors='black', linewidth=1.5, alpha=0.3, zorder=zorder-1)

ax1.set_aspect('equal')
ax1.set_title("Top View (a-b plane)")
ax1.set_xlabel(r"$\mathbf{x}$ ($\mathbf{\AA}$)")
ax1.set_ylabel(r"$\mathbf{y}$ ($\mathbf{\AA}$)")

# Tight Limits to remove whitespace
# a ~ 3.5, b ~ 6.3
ax1.set_xlim(-0.5, 5.0) # slightly more than 1 unit cell width
ax1.set_ylim(-1.0, 8.0) # slightly more than 1 unit cell height
# Actually, showing 2x2 is better for pattern recognition (zigzag)
ax1.set_xlim(-1, 8.0) 
ax1.set_ylim(-1, 14.0)

# --- SUBPLOT 2: SIDE VIEW (Buckling Focus) ---
# Previous issue: Too much vacuum.
# Fix: Zoom in on z [-2, 4]
ax2 = fig.add_subplot(1, 2, 2)
for atom in atoms:
    color = '#2c3e50' if atom['s'] == 'W' else '#f39c12'
    size = 600 if atom['s'] == 'W' else 300
    x, y, z = atom['pos']
    
    # y vs z
    ax2.scatter(y, z, c=color, s=size, edgecolors='black', linewidth=1.5)
    
    # Repeats in y
    shifts_y = [-1, 0, 1]
    for sy in shifts_y:
        if sy == 0: continue
        dy = sy * np.linalg.norm(cell[1])
        ax2.scatter(y + dy, z, c=color, s=size, edgecolors='black', linewidth=1.5, alpha=0.3)

ax2.set_aspect('equal')
ax2.set_title("Side View (Buckling)")
ax2.set_xlabel(r"$\mathbf{y}$ ($\mathbf{\AA}$)")
ax2.set_ylabel(r"$\mathbf{z}$ ($\mathbf{\AA}$)")

# CRITICAL: Remove Vacuum Whitespace
# Monolayer is at z~0 (or centered). If coordinates are raw, ensure we capture them.
# W is usually at 0, Te at +/- something.
z_coords = [a['pos'][2] for a in atoms]
z_cen = np.mean(z_coords)
ax2.set_ylim(z_cen - 3.0, z_cen + 3.0) # 6 Angstrom window vs 20 Angstrom cell!
ax2.set_xlim(-1, 14.0) # Match y scale roughly

# Add Annotation for Buckling
# Find a W and a Te
# ax2.annotate("Te", xy=(...), fontsize=20)
ax2.text(0.05, 0.9, "Vacuum Space Removed", transform=ax2.transAxes, fontsize=14, color='gray', style='italic')

# Save
OUT_FILE = 'repo/figures/Fig_Structure_Presentation.png'
# Handle output path robustly
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# If running script directly, script_dir might be current dir if __file__ is relative
# We assume we run from project root, but output needs to be correct.
if not os.path.exists('repo/figures'):
    os.makedirs('repo/figures')

plt.tight_layout()
plt.savefig(OUT_FILE, dpi=300)
print(f"Saved {OUT_FILE}")
