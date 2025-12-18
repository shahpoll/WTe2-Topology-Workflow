import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

# --- STYLE SETTINGS ---
params = {
    'figure.figsize': (16, 8),
    'font.family': 'sans-serif',
    'font.weight': 'bold',
    'font.size': 20,
    'axes.labelsize': 22,
    'lines.linewidth': 3,
}
plt.rcParams.update(params)

def plot_phase_comparison():
    # --- CONFIGURATION ---
    # Grid of W atoms
    nx, ny = 4, 3
    a = 1.0 # Lattice constant
    dx = a
    dy = a * np.sqrt(3)/2
    
    # Common settings for flipbook alignment
    xlims = (-1, nx*dx + 0.5) 
    ylims = (-1, ny*dy + 0.5)
    
    # --- 1. Ideal 1T Phase Data ---
    x_ideal = []
    y_ideal = []
    for j in range(ny):
        shift = 0.5 * dx if j % 2 else 0
        for i in range(nx):
            x_ideal.append(i*dx + shift)
            y_ideal.append(j*dy)
    
    # --- 2. 1T' Phase Data ---
    x_dist = []
    y_dist = []
    delta = 0.15 
    for j in range(ny):
        shift = 0.5 * dx if j % 2 else 0
        for i in range(nx):
            # Base
            base_x = i*dx + shift
            base_y = j*dy
            # Distortion
            zigzag_shift = -delta if i % 2 == 0 else delta
            x_dist.append(base_x + zigzag_shift * 0.5)
            y_dist.append(base_y)

    out_dir = os.path.dirname(os.path.abspath(__file__)) + "/../figures"
    if not os.path.exists(out_dir): os.makedirs(out_dir)

    # --- PLOT 1: 1T (Ideal) ---
    fig1, ax1 = plt.subplots(figsize=(10, 8))
    
    # Plot Atoms
    ax1.scatter(x_ideal, y_ideal, s=800, c='#2c3e50', edgecolors='black', label='W Atom')
    
    # Plot Bonds
    for i in range(len(x_ideal)):
        p1 = np.array([x_ideal[i], y_ideal[i]])
        for j in range(i+1, len(x_ideal)):
            p2 = np.array([x_ideal[j], y_ideal[j]])
            d = np.linalg.norm(p1 - p2)
            if d < 1.1 * a:
                ax1.plot([p1[0], p2[0]], [p1[1], p2[1]], color='gray', alpha=0.4, lw=3)
    
    # Styling
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_xlim(xlims)
    ax1.set_ylim(ylims)
    
    # Legend (Unified items mostly to keep size similar)
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Tungsten (W)',
               markerfacecolor='#2c3e50', markersize=25, markeredgecolor='black'),
        Line2D([0], [0], color='gray', lw=3, label='Isotropic Bond'),
    ]
    # Fixed location to prevent jumping
    ax1.legend(handles=legend_elements, loc='lower center', ncol=2, fontsize=20, bbox_to_anchor=(0.5, 0.02))
    
    plt.tight_layout()
    fig1.savefig(f"{out_dir}/Fig_Phase_1T.png", dpi=200)
    print(f"Saved {out_dir}/Fig_Phase_1T.png")
    
    # --- PLOT 2: 1T' (Distorted) ---
    fig2, ax2 = plt.subplots(figsize=(10, 8))
    
    ax2.scatter(x_dist, y_dist, s=800, c='#2c3e50', edgecolors='black')
    
    for i in range(len(x_dist)):
        p1 = np.array([x_dist[i], y_dist[i]])
        for j in range(i+1, len(x_dist)):
            p2 = np.array([x_dist[j], y_dist[j]])
            d = np.linalg.norm(p1 - p2)
            if d < 1.0 * a: 
                ax2.plot([p1[0], p2[0]], [p1[1], p2[1]], color='#e74c3c', alpha=1.0, lw=8) # Zigzag
            elif d < 1.2 * a:
                ax2.plot([p1[0], p2[0]], [p1[1], p2[1]], color='gray', alpha=0.2, lw=2)
                
    ax2.set_aspect('equal')
    ax2.axis('off')
    ax2.set_xlim(xlims) 
    ax2.set_ylim(ylims)
    
    legend_elements2 = [
        Line2D([0], [0], marker='o', color='w', label='Tungsten (W)',
               markerfacecolor='#2c3e50', markersize=25, markeredgecolor='black'),
        Line2D([0], [0], color='#e74c3c', lw=8, label='Zigzag Bond'),
    ]
    ax2.legend(handles=legend_elements2, loc='lower center', ncol=2, fontsize=20, bbox_to_anchor=(0.5, 0.02))

    plt.tight_layout()
    fig2.savefig(f"{out_dir}/Fig_Phase_1T_Prime.png", dpi=200)
    print(f"Saved {out_dir}/Fig_Phase_1T_Prime.png")


if __name__ == "__main__":
    plot_phase_comparison()
