import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# --- HARDCODED GEOMETRY (From your Methods Table) ---
# a=3.49, b=6.33, c=20.0
# Fractional coords (Approx from standard 1T')
# W (0.5, 0.28, 0.5), W (0.0, 0.78, 0.5) ... 
# (We will parse the file for exactness if possible, but let's use the known positions from the input file you have)

def parse_geometry(filename):
    atoms = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        in_atoms = False
        for line in lines:
            if "ATOMIC_POSITIONS" in line:
                in_atoms = True
                continue
            if in_atoms and len(line.split()) >= 4:
                parts = line.split()
                species = parts[0]
                # Assuming crystal coordinates
                try:
                    x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                    atoms.append({'s': species, 'x': x, 'y': y, 'z': z})
                except ValueError:
                    continue
            if in_atoms and (line.strip() == "" or "K_POINTS" in line):
                break
    return atoms

atoms = parse_geometry('wte2.scf.in')
# Lattice vectors (Orthorhombic approx for plotting)
lat_a, lat_b, lat_c = 3.49, 6.33, 20.0

fig = plt.figure(figsize=(8, 4)) # Reduced size from (10,5)

# --- SUBPLOT 1: TOP VIEW ---
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
for atom in atoms:
    color = 'blue' if atom['s'] == 'W' else 'orange'
    size = 100 if atom['s'] == 'W' else 50
    # Expand to 2x2 supercell for visualization of chains
    for dx in [0, 1]:
        for dy in [0, 1]:
            ax1.scatter((atom['x']+dx)*lat_a, (atom['y']+dy)*lat_b, atom['z']*lat_c, 
                       c=color, s=size, edgecolors='black', alpha=0.9)

ax1.view_init(elev=90, azim=-90) # Top View
ax1.set_title("Top View (Zigzag W Chains)", y=-0.1) # Lowered title
ax1.set_xlabel("a (Å)")
ax1.set_ylabel("b (Å)")
ax1.set_zticks([]) # Hide Z axis for 2D feel

# --- SUBPLOT 2: SIDE VIEW ---
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
for atom in atoms:
    color = 'blue' if atom['s'] == 'W' else 'orange'
    size = 100 if atom['s'] == 'W' else 50
    ax2.scatter(atom['x']*lat_a, atom['y']*lat_b, atom['z']*lat_c, 
               c=color, s=size, edgecolors='black')

ax2.view_init(elev=0, azim=0) # Side View
ax2.set_title(f"Side View (Vacuum ~ {lat_c*0.8:.1f} Å)", y=-0.1) # Lowered title
ax2.set_zlabel("c (Å)")
ax2.set_yticks([])

plt.subplots_adjust(wspace=0.0) # Bring plots closer
plt.tight_layout()
plt.savefig("Fig_Structure_Views.png", dpi=300)
print("Structure plot generated: Fig_Structure_Views.png")
