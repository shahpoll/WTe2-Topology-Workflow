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
    
    # Create Broad Grid and then Geometrically Filter
    # We want a clean strip along Y.
    nx_range = range(-4, 6)
    ny_range = range(-4, 10)
    
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
    species = np.array(species)
    
    # --- DEFINE RECTANGULAR CELL (Match 1T') ---
    u_rect = a1
    v_rect = a1 + 2*a2
    
    # "Reference Origin" for the box (before shift).
    # We pick (0,0,0) as the anchor for the Primary Cell calculation.
    ref_origin = np.array([0., 0., 0.])
    
    x_limit = np.linalg.norm(u_rect) 
    y_limit = np.linalg.norm(v_rect)
    
    # Find Primary Atoms (Pre-Shift) for Alignment Calculation
    # These are the ones inside the "Red Box" at i=0, j=0.
    primary_mask_pre = []
    
    for idx, (x, y, z) in enumerate(coords):
        rx = x - ref_origin[0]
        ry = y - ref_origin[1]
        tol = 0.1
        if (-tol <= rx <= x_limit + tol) and (-tol <= ry <= y_limit + tol):
            primary_mask_pre.append(idx)
            
    # --- COORDINATE ALIGNMENT ---
    # Calculate Centroid of these Primary Atoms
    primary_atom_coords = coords[primary_mask_pre]
    if len(primary_atom_coords) == 0:
        # Fallback if loops didn't cover (0,0) - shouldn't happen
        current_centroid = np.mean(coords, axis=0)
    else:
        current_centroid = np.mean(primary_atom_coords, axis=0)
    
    # Target Centroid (from 1T' Debug)
    target_primary_centroid = np.array([1.745, 4.706, 10.16])
    
    shift = target_primary_centroid - current_centroid
    coords += shift
    
    # Apply shift to reference origin (for drawing box)
    box_origin = ref_origin + shift
    # Project box origin Z to mean Z
    box_origin[2] = np.mean(coords[:, 2])

    
    # --- GEOMETRIC FILTERING (The "Ribbon" Cut) ---
    # User wants to keep atoms along Y axis, removing clutter.
    # 1T' Visual Bounds: X[-0.1, 5.75], Y[0.82, 12.92]
    # We will exclude anything significantly outside this strip.
    
    # Filter Limits
    x_min_f, x_max_f = -1.5, 6.0  # Slightly wider than view to avoid edge popping
    y_min_f, y_max_f = -1.0, 14.0 # Strip along Y
    
    final_coords = []
    final_species = []
    final_is_primary = []
    
    # Re-evaluate logic on shifted coords
    for idx, (x, y, z) in enumerate(coords):
        # 1. VISIBILITY CHECK
        if (x_min_f <= x <= x_max_f) and (y_min_f <= y <= y_max_f):
            final_coords.append([x, y, z])
            final_species.append(species[idx])
            
            # 2. PRIMARY (RED BOX) CHECK
            # Check if this specific atom was part of our "Primary" set?
            # Or just re-check if inside the shifted box?
            # Re-checking shifted box is robust.
            
            # Position relative to shifted box origin
            rx = x - box_origin[0]
            ry = y - box_origin[1]
            tol = 0.1
            in_box = (-tol <= rx <= x_limit + tol) and (-tol <= ry <= y_limit + tol)
            final_is_primary.append(in_box)
            
    final_coords = np.array(final_coords)
    
    # --- PLOTTING ---
    
    # Plot Atoms
    if len(final_coords) > 0:
        xs = final_coords[:, 0]
        ys = final_coords[:, 1]
        zs = final_coords[:, 2]
        
        for idx in range(len(final_coords)):
            x, y, z = xs[idx], ys[idx], zs[idx]
            atom = final_species[idx]
            is_primary = final_is_primary[idx]
    
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
        
    # Plot Bonds (Re-calc on visible atoms)
    bond_cutoff = 3.2 # Slightly larger to catch bonds
    
    # Optimization: Only loop visible atoms
    n_vis = len(final_coords)
    w_indices = [k for k, s in enumerate(final_species) if s == 'W']
    te_indices = [k for k, s in enumerate(final_species) if s == 'Te']
    
    for i in w_indices:
        p1 = final_coords[i]
        for j in te_indices:
            p2 = final_coords[j]
            dist = np.linalg.norm(p1 - p2)
            if dist < bond_cutoff:
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
    # Pull Z label closer to avoid clipping
    ax.set_zlabel(r"$z$ ($\AA$)", labelpad=8) 
    
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
    # Increase pad_inches to ensure Z label is saved
    plt.savefig(f"{out_dir}/Fig_Structure_3D_1T.png", dpi=300, bbox_inches='tight', pad_inches=0.1)
    print(f"Saved {out_dir}/Fig_Structure_3D_1T.png")

if __name__ == "__main__":
    plot_1T_3d()
