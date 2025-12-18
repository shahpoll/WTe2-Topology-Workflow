import matplotlib.pyplot as plt
import numpy as np
import os

# --- STYLE SETTINGS (MATCHING 1T' SCRIPT) ---
params = {
    'figure.figsize': (10, 8),
    'font.family': 'sans-serif',
    'font.weight': 'bold',
    'font.size': 16,
    'axes.labelsize': 18,
    'lines.linewidth': 2,
}
plt.rcParams.update(params)

def plot_1T_3d():
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # --- 1T GEOMETRY (Ideal Octahedral) ---
    # a = b approx 3.5 A
    a_lat = 3.52 
    
    # Hexagonal Lattice Vectors
    # a1 = (a, 0, 0)
    # a2 = (-a/2, a*sqrt(3)/2, 0)
    a1 = np.array([a_lat, 0, 0])
    a2 = np.array([-a_lat/2, a_lat * np.sqrt(3)/2, 0])
    c_vec = np.array([0, 0, 15.0]) # Vacuum
    
    # Atomic Basis (Monolayer 1T)
    # W at (0,0,0)
    # Te at (1/3, 2/3, z) and (2/3, 1/3, -z)
    z_te = 1.6 # Approx height
    
    coords = []
    species = []
    
    # Create 2x2 supercell for visualization (Matches 1T' better)
    nx, ny = 2, 2
    
    for i in range(-1, nx-1):
        for j in range(-1, ny-1):
            # Origin of cell
            origin = i*a1 + j*a2
            
            # W Atom
            w_pos = origin
            coords.append(w_pos)
            species.append('W')
            
            # Te Top
            te1_pos = origin + (1.0/3.0)*a1 + (2.0/3.0)*a2 + np.array([0, 0, z_te])
            coords.append(te1_pos)
            species.append('Te')
            
            # Te Bottom
            te2_pos = origin + (2.0/3.0)*a1 + (1.0/3.0)*a2 + np.array([0, 0, -z_te])
            coords.append(te2_pos)
            species.append('Te')
            
    coords = np.array(coords)
    
    # --- PLOTTING ---
    
    # Plot Atoms with Highlight Logic
    # 1T Logic: We manually built a 3x3 supercell.
    # Indices: i ranges -1 to nx-1 (-1, 0, 1). j ranges -1 to ny-1 (-1, 0, 1).
    # We want the Central Cell (i=0, j=0) highlighted.
    
    for idx, (x, y, z) in enumerate(coords): # idx isn't loop var, enumerate
        # Recover i,j from order? 
        # Loop structure was: for i... for j... 
        # i runs -1, 0, 1. j runs -1, 0, 1.
        # Total 9 cells. i=0, j=0 is the 5th cell (index 4) if flattened?
        # Actually simplest is to check position!
        # Highlighting atom near origin (0,0)
        
        # Check if approx inside Unit Cell parallelogram?
        # Unit cell vectors a1, a2.
        # Check if x*a1 + y*a2?
        # Simple distance check from Origin is easiest for visuals.
        # But cell 0,0 starts at origin.
        
        # We manually constructed the list.
        # Let's count. 
        # i ranges -1..0 (2 values). j ranges -1..0 (2 values). 4 cells total.
        # 12 atoms total.
        # The (0,0) cell is the 4th cell (index 3).
        # Atoms 9, 10, 11.
        
        floor_idx = idx // 3 # Which cell number
        # Cell order: 
        # i=-1, j=-1 (0)   #0
        # i=-1, j=0  (1)   #1
        # i=0,  j=-1 (2)   #2
        # i=0,  j=0  (3)   #3 -> TARGET (Central)
        
        # nx=2, ny=2. Loop i: -1, 0. j: -1, 0.
        # ij pairs: (-1,-1), (-1,0), (0,-1), (0,0)
        # Total 4 cells.
        # Index 3 is (0,0).
        
        is_primary = (floor_idx == 3)

        atom = species[idx]
        if atom == 'W':
            base_color = '#2c3e50'
        else:
            base_color = '#f39c12'
            
        if is_primary:
            color = base_color
            alpha = 1.0
            edgecolor = 'black'
        else:
            if atom == 'W': color = '#bdc3c7'
            else: color = '#fcd088'
            alpha = 0.8
            edgecolor = 'gray'
            
        size = 400 if atom == 'W' else 300
        zorder = 10 if atom == 'W' else 9
            
        ax.scatter(x, y, z, s=size, c=color, edgecolors=edgecolor, alpha=1.0, zorder=zorder)
        
    # Plot Bonds
    # 1T Coordination: Each W connected to 6 Te (3 top, 3 bottom)
    # Cutoff distance
    bond_cutoff = 3.0
    
    # Iterate over W atoms and find Te neighbors
    w_indices = [k for k, s in enumerate(species) if s == 'W']
    te_indices = [k for k, s in enumerate(species) if s == 'Te']
    
    for i in w_indices:
        p1 = coords[i]
        for j in te_indices:
            p2 = coords[j]
            dist = np.linalg.norm(p1 - p2)
            if dist < bond_cutoff:
                # 1T Bonds are all identical (gray)
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 
                       color='gray', alpha=0.4, linewidth=2)

    # Unit Cell Box (for center cell)
    # 0,0 to 1,0 to 1,1 to 0,1
    # Just draw a rhombus on the plane z=0?
    # Or simple box. Let's draw the "Unit Cell" outline for clarity.
    cell_origin = np.array([0, 0, 0])
    # Rhombus
    uc_corners = [
        cell_origin,
        cell_origin + a1,
        cell_origin + a1 + a2,
        cell_origin + a2,
        cell_origin
    ]
    uc_x = [p[0] for p in uc_corners]
    uc_y = [p[1] for p in uc_corners]
    uc_z = [0]*5
    ax.plot(uc_x, uc_y, uc_z, color='red', linestyle='--', linewidth=2, label='Unit Cell')
    

    # --- CAMERA & LIMITS ---
    # Match the 3D 1T' view roughly
    # elev=30, azim=-60 is standard isometric
    ax.view_init(elev=30, azim=-60)
    
    # Aspect Ratio - FIXED MATCHING 1T'
    # Range X~7, Y~8, Z~5
    ax.set_box_aspect((7.5, 8.5, 5.0))
    
    # Limits - FIXED MATCHING 1T'
    ax.set_xlim(-2, 8)
    ax.set_ylim(-4, 6)
    ax.set_zlim(-3, 3)
    
    ax.set_axis_off()
    
    # Labels
    ax.set_xlabel(r"$x$ ($\AA$)", labelpad=10)
    ax.set_ylabel(r"$y$ ($\AA$)", labelpad=10)
    ax.set_zlabel(r"$z$ ($\AA$)", labelpad=25)
    ax.set_title(r"1T-WTe$_2$ (Ideal)", pad=0, fontsize=24)
    
    # Limits - FIXED MATCHING 1T' (Tighter)
    ax.set_xlim(-0.5, 7.0)
    ax.set_ylim(-1.0, 7.5)
    ax.set_zlim(-2.5, 2.5)
    
    ax.set_axis_off() # This line was duplicated, keeping the one from the instruction.
    
    out_dir = os.path.dirname(os.path.abspath(__file__)) + "/../figures"
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    plt.savefig(f"{out_dir}/Fig_Structure_3D_1T.png", dpi=300, bbox_inches='tight', pad_inches=0.02)
    print(f"Saved {out_dir}/Fig_Structure_3D_1T.png")

if __name__ == "__main__":
    plot_1T_3d()
