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
    px = [0, 0.5, 0.5, 0, 0]
    py = [0, 0, 0.5*aspect, 0.5*aspect, 0]
    
    plt.plot(px, py, color='#D50032', linewidth=2, linestyle='--', zorder=2, label='Band Path')
    
    for label, (x, y) in points.items():
        plt.scatter(x, y, color='#003366', s=150, zorder=3, edgecolor='white')
        # Offsets
        ox = 0.03 if x < 0.3 else -0.06
        oy = 0.03*aspect if y < 0.2 else -0.08*aspect
        if 'Gamma' in label: ox, oy = 0.02, 0.02
        plt.text(x+ox, y+oy, label, fontsize=16, fontweight='bold', zorder=4)

    ax.set_xlim(-0.6, 0.6)
    ax.set_ylim(-0.6*aspect, 0.6*aspect)
    ax.axis('off')
    plt.title("First Brillouin Zone (Scaled)", fontsize=14)
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=300)
    print(f"Scaled BZ schematic saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    plot_bz()
