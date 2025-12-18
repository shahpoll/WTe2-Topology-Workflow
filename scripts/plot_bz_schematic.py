import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# --- CONFIGURATION ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "../figures/Fig_BZ_Schematic.png")

def plot_bz():
    # Lattice Constants (Angstrom)
    a, b = 3.49, 6.33
    
    # Reciprocal Lattice proportional to 1/a and 1/b
    # k_x range ~ 1/a = 0.28
    # k_y range ~ 1/b = 0.15
    # Aspect Ratio = (1/b) / (1/a) = a/b
    aspect = a / b # ~0.55 (Height vs Width)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Draw Rectangle (Centered at 0,0)
    # Width = 1.0 (Normalized), Height = aspect
    rect = patches.Rectangle((-0.5, -0.5*aspect), 1.0, aspect, 
                             linewidth=2, edgecolor='black', facecolor='#F5F5F5', zorder=1)
    ax.add_patch(rect)
    
    # Points
    points = {
        r'$\Gamma$': (0, 0),
        'X': (0.5, 0),
        'Y': (0, 0.5*aspect),
        'M': (0.5, 0.5*aspect)
    }
    
    # Path
    # Path: Gamma -> X -> M -> Gamma -> Y
    # Gamma=(0,0), X=(0.5,0), M=(0.5, 0.5*aspect), Y=(0, 0.5*aspect)
    # Path: Gamma -> X -> M -> Gamma -> Y
    # Segment 1: Gamma -> X -> M -> Gamma (Closed Triangle)
    px1 = [0, 0.5, 0.5, 0]
    py1 = [0, 0, 0.5*aspect, 0]
    
    # Segment 2: Gamma -> Y (Vertical Line)
    px2 = [0, 0]
    py2 = [0, 0.5*aspect]
    
    plt.plot(px1, py1, color='#D50032', linewidth=2, linestyle='--', zorder=2, label='Band Path Main')
    plt.plot(px2, py2, color='#D50032', linewidth=2, linestyle='--', zorder=2, label='Band Path Y-Leg')
    
    # Add Directional Arrows to Path
    # Function to add arrow at midpoint
    def add_path_arrow(start, end):
        mx = (start[0] + end[0]) / 2
        my = (start[1] + end[1]) / 2
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        plt.arrow(mx - dx*0.1, my - dy*0.1, dx*0.001, dy*0.001, 
                  shape='full', lw=0, length_includes_head=True, head_width=0.03, head_length=0.04, fc='#D50032', ec='#D50032', zorder=5)

    # Segments: Gamma->X, X->M, M->Gamma, Gamma->Y
    add_path_arrow((0,0), (0.5,0))          # Gamma -> X
    add_path_arrow((0.5,0), (0.5, 0.5*aspect)) # X -> M
    add_path_arrow((0.5, 0.5*aspect), (0,0))   # M -> Gamma
    add_path_arrow((0,0), (0, 0.5*aspect))     # Gamma -> Y
    
    # Point Labels
    for label, (x, y) in points.items():
        plt.scatter(x, y, color='#003366', s=120, zorder=3, edgecolor='white', linewidth=1.5)
        # Offsets
        ox = 0.03 if x < 0.3 else -0.06
        oy = 0.03*aspect if y < 0.2 else -0.08*aspect
        
        # Gamma: Use LaTeX bold for thickness
        if 'Gamma' in label: 
            label = r'$\mathbf{\Gamma}$'
            ox, oy = 0.02, -0.08*aspect
            
        plt.text(x+ox, y+oy, label, fontsize=20, fontweight='bold', zorder=4)

    ax.set_xlim(-0.6, 0.6)
    ax.set_ylim(-0.6*aspect, 0.6*aspect)
    ax.axis('off')
    
    # Axis Arrows (Thinner, cleaner)
    # Move text further away to avoid overlap
    ax.arrow(-0.55, -0.55*aspect, 0.2, 0, head_width=0.03, head_length=0.03, fc='k', ec='k', lw=1.5)
    ax.arrow(-0.55, -0.55*aspect, 0, 0.2*aspect, head_width=0.03, head_length=0.03, fc='k', ec='k', lw=1.5)
    
    # Kx and Ky Labels (Bold and positioned to clear arrows)
    ax.text(-0.32, -0.62*aspect, r'$\mathbf{k_x}$', fontsize=20)
    # Moved ky up (from -0.35*aspect to -0.25*aspect)
    ax.text(-0.62, -0.25*aspect, r'$\mathbf{k_y}$', fontsize=20)

    plt.title("First Brillouin Zone (Scaled)", fontsize=18, pad=15)
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=300)
    print(f"Scaled BZ schematic saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    plot_bz()
