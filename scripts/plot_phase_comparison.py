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
    fig, (ax1, ax2) = plt.subplots(1, 2)
    
    # --- 1. Ideal 1T Phase (High Symmetry) ---
    # Triangular Lattice of Tungsten (W)
    # Hexagonal arrangement
    
    # Grid of W atoms
    nx, ny = 4, 3
    x_ideal = []
    y_ideal = []
    
    # Triangular lattice: odd rows shifted
    a = 1.0 # Lattice constant
    dx = a
    dy = a * np.sqrt(3)/2
    
    for j in range(ny):
        shift = 0.5 * dx if j % 2 else 0
        for i in range(nx):
            x_ideal.append(i*dx + shift)
            y_ideal.append(j*dy)
            
    # Plot W Atoms
    ax1.scatter(x_ideal, y_ideal, s=600, c='#2c3e50', edgecolors='black', label='W Atom')
    
    # Draw Bonds (Isotropic)
    # Connect neighbors
    for i in range(len(x_ideal)):
        p1 = np.array([x_ideal[i], y_ideal[i]])
        for j in range(i+1, len(x_ideal)):
            p2 = np.array([x_ideal[j], y_ideal[j]])
            d = np.linalg.norm(p1 - p2)
            if d < 1.1 * a: # Nearest neighbor
                ax1.plot([p1[0], p2[0]], [p1[1], p2[1]], color='gray', alpha=0.4, lw=2)
                
    ax1.set_title("1T Phase (Ideal)\nHigh Symmetry")
    ax1.set_aspect('equal')
    ax1.axis('off')
    
    # Annotation
    ax1.text(1.5, -0.5, "Isotropic Triangular Lattice", ha='center', fontsize=18, style='italic', color='#555')
    
    # --- 2. 1T' Phase (Distorted) ---
    # Peierls Distortion: W atoms dimerize along x
    # Zigzag chains
    
    x_dist = []
    y_dist = []
    
    # Distortion parameter
    delta = 0.15 
    
    for j in range(ny):
        shift = 0.5 * dx if j % 2 else 0
        for i in range(nx):
            # Distortion logic:
            # Shift atoms towards each other in pairs?
            # Or simplified: Zigzag logic.
            # In 1T', W chains run along one axis (say y) and zigzag in x?
            # Actually, standard view is chains along a (x).
            # Let's simulate the Zigzag chain.
            
            # Base position
            base_x = i*dx + shift
            base_y = j*dy
            
            # Apply y-dependent x-shift to create zigzag
            # Row 0: shift right. Row 1: shift left.
            # This makes the "chain" look wavy if we connect vertically?
            # NO, the chain is usually along the a-axis.
            # Dimerization along a-axis:
            # x positions: 0, 1 -> 0+d, 1-d (Short bond)
            
            # Simple 1D Peierls:
            zigzag_shift = -delta if i % 2 == 0 else delta
            
            # But 1T' WTe2 has zigzag chains mostly isolated.
            # Let's just create the visual "Zigzag" look.
            # Move row 0 up, row 1 down?
            # Let's stick to the canonical "Buckled Zigzag Chain".
            
            # Simplified Schematic:
            # Just show the bonds.
            
            new_x = base_x + zigzag_shift * 0.5 # Small x dimerization
            new_y = base_y
            
            # Also y-buckling? Let's keep it 2D for clarity.
            
            x_dist.append(new_x)
            y_dist.append(new_y)
            
    ax2.scatter(x_dist, y_dist, s=600, c='#2c3e50', edgecolors='black')
    
    # Draw Distorted Bonds
    # The key feature is the W-W chain formation
    for i in range(len(x_dist)):
        p1 = np.array([x_dist[i], y_dist[i]])
        for j in range(i+1, len(x_dist)):
            p2 = np.array([x_dist[j], y_dist[j]])
            d = np.linalg.norm(p1 - p2)
            
            # Highlight Short Bonds (The Dimer/Chain)
            if d < 1.0 * a: # Shortened bond
                ax2.plot([p1[0], p2[0]], [p1[1], p2[1]], color='#e74c3c', alpha=1.0, lw=5) # RED thick bond
            elif d < 1.2 * a: # Other neighbors
                ax2.plot([p1[0], p2[0]], [p1[1], p2[1]], color='gray', alpha=0.2, lw=1)
                
    ax2.set_title(r"1T' Phase (Distorted)" + "\nTopology Enabler")
    ax2.set_aspect('equal')
    ax2.axis('off')
    
    ax2.text(1.5, -0.5, "Peierls Distortion (Zigzag Chains)", ha='center', fontsize=18, style='italic', color='#555')
    
    # --- LEGEND & ANNOTATIONS ---
    # Legend for W Atom
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Tungsten (W) Atom',
               markerfacecolor='#2c3e50', markersize=25, markeredgecolor='black'),
        Line2D([0], [0], color='#e74c3c', lw=5, label='Dimerized Bond (Zigzag)'),
    ]
    
    # Place legend on the second plot or unified?
    # Unified legend at bottom center
    fig.legend(handles=legend_elements, loc='lower center', ncol=2, fontsize=20, bbox_to_anchor=(0.5, 0.05))
    
    # Adjust layout to make room for legend
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2) # Make space at bottom
    
    # Output
    out_dir = os.path.dirname(os.path.abspath(__file__)) + "/../figures"
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    plt.savefig(f"{out_dir}/Fig_Phase_Comparison.png", dpi=200)
    print(f"Saved {out_dir}/Fig_Phase_Comparison.png")

if __name__ == "__main__":
    plot_phase_comparison()
