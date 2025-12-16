import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# --- CONFIGURATION FOR PRESENTATION ---
# Robust paths relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "../data/wte2_band.dat")
LABEL_FILE = os.path.join(SCRIPT_DIR, "../data/wte2_band.labelinfo.dat")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "../figures/Fig_Bands_Presentation.png")

# Presentation "Big Mode" Settings
params = {
    'axes.labelsize': 20,
    'axes.titlesize': 24,
    'xtick.labelsize': 18,
    'ytick.labelsize': 18,
    'lines.linewidth': 2.5,
    'figure.figsize': (10, 6),
    'font.family': 'sans-serif', # Sans-serif is better for slides
    'font.weight': 'bold'
}
plt.rcParams.update(params)

def parse_labels(labelfile):
    """Parses the high-symmetry point labels and coordinates."""
    ticks = []
    labels = []
    if not os.path.exists(labelfile):
        print(f"Warning: {labelfile} not found. Using default placeholders.")
        # Fallback based on typical path if file missing
        return [0.0, 1.0, 2.0, 3.0], [r'$\Gamma$', 'X', 'M', r'$\Gamma$']
    
    with open(labelfile, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 2:
            # Usually format: "Label  Coordinate" or "Coordinate Label"
            try:
                # Try reading 2nd column as float (standard QE 'bands.out.gnu' labels often are " " "quoted" or just text)
                # But wte2_band.labelinfo.dat from simple script usually: "Label k-coord"
                # Let's inspect typical content if we fail, but try-except is good.
                
                # Check which one is float
                try:
                    pos = float(parts[1])
                    lbl = parts[0]
                except ValueError:
                    pos = float(parts[0])
                    lbl = parts[1]
            except ValueError:
                continue

            # Formatting Gamma
            if 'G' in lbl or 'gamma' in lbl.lower():
                lbl = r'$\mathbf{\Gamma}$'
            else:
                 lbl = r'$\mathbf{' + lbl + r'}$'
            
            ticks.append(pos)
            labels.append(lbl)
    return ticks, labels

def plot_bands():
    print(f"Reading data from {DATA_FILE}")
    # 1. Load Band Data
    try:
        data = np.loadtxt(DATA_FILE)
    except Exception as e:
        print(f"Error reading data: {e}")
        return

    k = data[:, 0]
    energy = data[:, 1]
    
    # Identify unique band segments (Wannier90 separates bands with blank lines or jumps)
    # or Gnuplot format.
    bands = []
    current_band_k = []
    current_band_e = []
    
    # Re-reading file safely to handle blank lines splitting
    with open(DATA_FILE, 'r') as f:
        for line in f:
            if not line.strip(): # Empty line
                if current_band_k:
                    bands.append((current_band_k, current_band_e))
                    current_band_k = []
                    current_band_e = []
                continue
            try:
                parts = line.split()
                current_band_k.append(float(parts[0]))
                current_band_e.append(float(parts[1]))
            except ValueError:
                 continue
                 
    if current_band_k: bands.append((current_band_k, current_band_e))

    # 2. Setup Plot
    fig, ax = plt.subplots()
    
    # 3. Plot Bands
    for bk, be in bands:
        ax.plot(bk, be, color='#333333', alpha=0.9) # Dark Grey/Black

    # 4. Fermi Level
    ax.axhline(0, color='#D50032', linestyle='--', linewidth=2, label='Fermi Level')

    # 5. Handle Ticks
    xticks, xlabels = parse_labels(LABEL_FILE)
    # Fallback if label file parsing failed implies we might want to manually set if we know the path
    # If using wte2_band.dat which is from Wannier90, the path is standard
    if len(xticks) < 2:
        k_max = bands[0][0][-1] if bands else 1.0
        xticks = [0, k_max * 0.25, k_max * 0.5, k_max * 0.75, k_max]
        xlabels = [r'$\mathbf{\Gamma}$', r'$\mathbf{X}$', r'$\mathbf{M}$', r'$\mathbf{\Gamma}$', r'$\mathbf{Y}$']

    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels)
    
    # Add vertical lines for High Symmetry Points
    for x in xticks:
        ax.axvline(x, color='gray', linestyle='-', linewidth=1, alpha=0.5)

    # 6. Limits & Labels
    ax.set_xlim(min(k), max(k))
    # Adjust Y-limits to focus on the gap (e.g., -1.5 to +1.5 eV)
    ax.set_ylim(-1.5, 1.5) 
    
    ax.set_ylabel(r'Energy ($E - E_F$) [eV]')
    # Remove X-axis label "Momentum" because the ticks are self-explanatory
    
    ax.set_title("Relativistic Electronic Structure", pad=20)

    # 7. Annotation (The "Money" Shot)
    # Point to the gap
    # Arrow properties
    ax.annotate('Inverted Gap', xy=(0, 0.1), xytext=(0.3, 0.6),
            arrowprops=dict(facecolor='#D50032', shrink=0.05, width=2),
            fontsize=16, color='#D50032', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=300)
    print(f"Presentation band structure saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    plot_bands()
