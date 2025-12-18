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
    
    # Create 3x3 supercell for visualization
    nx, ny = 3, 3
    
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
    
    # Plot Atoms
    for i, (x, y, z) in enumerate(coords):
        atom = species[i]
        if atom == 'W':
            color = '#2c3e50' # Dark Blue/Slate
            size = 400
            zorder = 10
        else: # Te
            color = '#f39c12' # Orange
            size = 300
            zorder = 9
            
        ax.scatter(x, y, z, s=size, c=color, edgecolors='black', alpha=1.0, zorder=zorder)
        
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
    
    # Limits - tight around 0,0
    limit = 5
    ax.set_xlim(-2, 6)
    ax.set_ylim(-2, 6)
    ax.set_zlim(-3, 3)
    
    ax.set_axis_off()
    
    # Title? Use Clean look.
    # ax.set_title("1T Phase (Ideal)", fontsize=24)
    
    out_dir = os.path.dirname(os.path.abspath(__file__)) + "/../figures"
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    plt.savefig(f"{out_dir}/Fig_Structure_3D_1T.png", dpi=300, bbox_inches='tight', pad_inches=0.1)
    print(f"Saved {out_dir}/Fig_Structure_3D_1T.png")

if __name__ == "__main__":
    plot_1T_3d()
