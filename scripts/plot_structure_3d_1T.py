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
    
    # Create Large Primitive Grid to ensure we fill the view
    # We will then select a central "Rectangular" cell to be the 'Primary' one.
    nx_range = range(-3, 4)
    ny_range = range(-2, 5)
    
    for i in nx_range:
        for j in ny_range:
            # Origin of cell
            origin = i*a1 + j*a2
            
            w_pos = origin
            coords.append(w_pos)
            species.append('W')
            
            te1_pos = origin + (1.0/3.0)*a1 + (2.0/3.0)*a2 + np.array([0, 0, z_te])
            coords.append(te1_pos)
            species.append('Te')
            
            te2_pos = origin + (2.0/3.0)*a1 + (1.0/3.0)*a2 + np.array([0, 0, -z_te])
            coords.append(te2_pos)
            species.append('Te')
            
    coords = np.array(coords)
    
    # --- DEFINE RECTANGULAR CELL (Match 1T') ---
    # The 1T' cell is roughly a 1x2 supercell of 1T.
    # a_rect = a1
    # b_rect = a1 + 2*a2 (Orthogonal to a1)
    
    u_rect = a1
    v_rect = a1 + 2*a2
    
    # Define the "Ideal" Box at the origin (0,0,0) initially
    # We want a box starting at origin containing the atoms.
    # For a perfect match, the box should be [0, u] x [0, v].
    
    # Identify atoms inside this Rectangular Box (Primary Cell)
    # We'll use dot products to project atoms relative to a chosen origin.
    # Let's pick origin such that it captures a nice full cell.
    # If we pick (0,0), the box includes (0,0) W and (1,1) W (skew).
    
    # Let's find atoms in the box defined by parallelogram of u_rect, v_rect.
    # Project coords onto normalized u and v?
    # Or just geometric check: 
    # pos = c1*u_rect + c2*v_rect. 0 <= c1 < 1, 0 <= c2 < 1.
    
    # Matrix M = [u, v, z_axis]. Inv(M) * pos = [c1, c2, c3]
    # u = [a, 0, 0]
    # v = [0, b, 0] (Since a1+2a2 is pure Y)
    # So simple x,y bounds!
    
    x_limit = np.linalg.norm(u_rect) # 3.53
    y_limit = np.linalg.norm(v_rect) # 6.12 approx
    
    # We need to pick a "Reference Origin" for the lattice to define the box.
    # Let's try picking one W atom near the middle of our generated cloud as the Box Origin.
    # Our loops went -3..4. (0,0) is in middle. Let's use (0,0) W atom as origin.
    ref_origin = np.array([0., 0., 0.])
    
    primary_indices = []
    
    for idx, (x, y, z) in enumerate(coords):
        # Relative pos
        rx = x - ref_origin[0]
        ry = y - ref_origin[1]
        
        # Check tolerance to include atoms ON the boundary (corners)
        # 1T' usually highlights the corner Ws + internal.
        tol = 0.1
        
        if (-tol <= rx <= x_limit + tol) and (-tol <= ry <= y_limit + tol):
            primary_indices.append(idx)
            
    # --- COORDINATE ALIGNMENT ---
    # Calculate Centroid of these Primary Atoms
    primary_atom_coords = coords[primary_indices]
    current_centroid = np.mean(primary_atom_coords, axis=0)
    
    # Target Centroid (from 1T' Debug)
    target_primary_centroid = np.array([1.745, 4.706, 10.16])
    
    shift = target_primary_centroid - current_centroid
    coords += shift
    
    # Apply shift to reference origin too (for drawing box)
    box_origin = ref_origin + shift
    # Project box origin Z to mean Z
    box_origin[2] = np.mean(coords[:, 2])

    
    # --- PLOTTING ---
    
    # Plot Atoms
    # Re-extract shifted columns for plotting
    xs = coords[:, 0]
    ys = coords[:, 1]
    zs = coords[:, 2]
    
    for idx, (x, y, z) in enumerate(coords):
        is_primary = (idx in primary_indices)

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

    # Unit Cell Box (Rectangular 1T' shape)
    uc_corners = [
        box_origin,
        box_origin + u_rect,
        box_origin + u_rect + v_rect,
        box_origin + v_rect,
        box_origin
    ]
    uc_x = [p[0] for p in uc_corners]
    uc_y = [p[1] for p in uc_corners]
    uc_z = [p[2] for p in uc_corners]
    ax.plot(uc_x, uc_y, uc_z, color='red', linestyle='--', linewidth=2, label='Unit Cell')

    # --- CAMERA & LIMITS (EXACT 1T' MATCH) ---
    ax.view_init(elev=30, azim=-60)
    
    # Hardcoded Dimensions from Debug
    ax.set_xlim(-0.1, 5.75)
    ax.set_ylim(0.82, 12.92)
    ax.set_zlim(6.96, 12.96)
    
    ax.set_box_aspect((0.80, 1.55, 0.77))
    
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.grid(False)
    
    # Labels
    ax.set_xlabel(r"$x$ ($\AA$)", labelpad=10)
    ax.set_ylabel(r"$y$ ($\AA$)", labelpad=10)
    ax.set_zlabel(r"$z$ ($\AA$)", labelpad=12)
    
    # Title
    ax.set_title(r"1T-WTe$_2$ (Ideal)", pad=-20, fontsize=24, y=1.02)
    
    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='W',
               markerfacecolor='#2c3e50', markersize=15, markeredgecolor='black'),
        Line2D([0], [0], marker='o', color='w', label='Te',
               markerfacecolor='#f39c12', markersize=12, markeredgecolor='black')
    ]
    ax.legend(handles=legend_elements, loc='upper left', frameon=False, fontsize=14)
    
    out_dir = os.path.dirname(os.path.abspath(__file__)) + "/../figures"
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    plt.savefig(f"{out_dir}/Fig_Structure_3D_1T.png", dpi=300, bbox_inches='tight', pad_inches=0.02)
    print(f"Saved {out_dir}/Fig_Structure_3D_1T.png")

if __name__ == "__main__":
    plot_1T_3d()
