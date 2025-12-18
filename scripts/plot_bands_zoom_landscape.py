import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# --- CONFIGURATION FOR PRESENTATION (LANDSCAPE ZOOM) ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "../data/wte2_band.dat")
LABEL_FILE = os.path.join(SCRIPT_DIR, "../data/wte2_band.labelinfo.dat")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "../figures/Fig_Bands_Zoom_Landscape.png")

# Wide Landscape Settings
params = {
    'axes.labelsize': 20,
    'axes.titlesize': 24,
    'xtick.labelsize': 18,
    'ytick.labelsize': 18,
    'lines.linewidth': 3.0, # Thicker lines for zoom
    'figure.figsize': (10, 4.5), # Wide and Short
    'font.family': 'sans-serif',
    'font.weight': 'bold'
}
plt.rcParams.update(params)

def parse_labels(labelfile):
    ticks = []
    labels = []
    if not os.path.exists(labelfile):
        # Fallback
        return [0.0, 1.0, 2.0, 3.0], [r'$\Gamma$', 'X', 'M', r'$\Gamma$']
    
    with open(labelfile, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 2:
            try:
                try:
                    pos = float(parts[1])
                    lbl = parts[0]
                except ValueError:
                    pos = float(parts[0])
                    lbl = parts[1]
            except ValueError:
                continue

            if 'G' in lbl or 'gamma' in lbl.lower():
                lbl = r'$\mathbf{\Gamma}$'
            else:
                 lbl = r'$\mathbf{' + lbl + r'}$'
            
            ticks.append(pos)
            labels.append(lbl)
    return ticks, labels

def plot_bands_zoom():
    print(f"Reading data from {DATA_FILE}")
    try:
        data = np.loadtxt(DATA_FILE)
    except Exception as e:
        print(f"Error reading data: {e}")
        return

    k = data[:, 0]
    
    bands = []
    current_band_k = []
    current_band_e = []
    
    with open(DATA_FILE, 'r') as f:
        for line in f:
            if not line.strip():
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

    fig, ax = plt.subplots()
    
    # Plot Bands
    for bk, be in bands:
        ax.plot(bk, be, color='#333333', alpha=0.9)

    # Fermi Level
    ax.axhline(0, color='#D50032', linestyle='--', linewidth=2, label='Fermi Level')

    # Ticks
    xticks, xlabels = parse_labels(LABEL_FILE)
    if len(xticks) < 2:
        k_max = bands[0][0][-1] if bands else 1.0
        xticks = [0, k_max * 0.25, k_max * 0.5, k_max * 0.75, k_max]
        xlabels = [r'$\mathbf{\Gamma}$', r'$\mathbf{X}$', r'$\mathbf{M}$', r'$\mathbf{\Gamma}$', r'$\mathbf{Y}$']

    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels)
    
    for x in xticks:
        ax.axvline(x, color='gray', linestyle='-', linewidth=1, alpha=0.5)

    # Limits - ZOOMED AND LANDSCAPE
    ax.set_xlim(min(k), max(k))
    ax.set_ylim(-0.6, 0.6) # Focus on the overlap
    
    ax.set_ylabel(r'Energy [eV]')
    ax.set_title("Zoom: Indirect Overlap", pad=15)

    # Highlight the Overlap
    # Add a shaded region or arrows
    # Q-point approx 0.3 along Gamma-X? No, usually Q is the local min.
    # We can just let the viewer see it.
    
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=300)
    print(f"Zoomed Landscape band structure saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    plot_bands_zoom()
