import matplotlib.pyplot as plt
import numpy as np

def parse_wannier_bands(filename):
    """
    Reads a standard Wannier90 band.dat file.
    Gnuplot format separates bands by blank lines.
    """
    bands = []
    current_band = []
    
    with open(filename, 'r') as f:
        for line in f:
            if not line.strip(): # Blank line = end of a band
                if current_band:
                    bands.append(np.array(current_band))
                    current_band = []
            else:
                try:
                    parts = line.split()
                    k = float(parts[0])
                    e = float(parts[1])
                    current_band.append([k, e])
                except ValueError:
                    continue
    if current_band:
        bands.append(np.array(current_band))
    return bands

# --- PLOTTING ---
filename = 'wte2_band.dat'
try:
    bands = parse_wannier_bands(filename)
    print(f"Loaded {len(bands)} bands.")
except FileNotFoundError:
    print("Error: wte2_band.dat not found.")
    exit()

fig, ax = plt.subplots(figsize=(6, 8))

# Plot each band as a smooth line
for band in bands:
    k = band[:, 0]
    e = band[:, 1]
    ax.plot(k, e, color='black', linewidth=1.2, alpha=0.8)

# --- CRITICAL FORMATTING FOR PRESENTATION ---
# 1. The Window: Focus on the "Action" (-0.5 to 0.5 eV)
ax.set_ylim(-0.6, 0.6)
ax.set_xlim(bands[0][0,0], bands[0][-1,0])

# 2. The Reference Line
ax.axhline(0, color='red', linestyle='--', linewidth=1, label='Fermi Level')

# 3. High Symmetry Labels (Manual Placement based on your k-path)
# Path: G -> X -> M -> G -> Y
# We assume equal spacing usually, but let's grab the max k
k_max = bands[0][-1,0]
# Approximate locations for standard 4-segment path
ticks = [0, k_max * 0.25, k_max * 0.5, k_max * 0.75, k_max]
labels = [r'$\mathbf{\Gamma}$', r'$\mathbf{X}$', r'$\mathbf{M}$', r'$\mathbf{\Gamma}$', r'$\mathbf{Y}$']
ax.set_xticks(ticks)
ax.set_xticklabels(labels, fontsize=18)
ax.tick_params(axis='both', which='major', labelsize=16, width=2, length=6)

# 4. Highlight the Inversion (The "Open" Gap)
# We expect the gap near Gamma (first and fourth tick)
ax.text(0.05, 0.15, "Inverted Gap", color='blue', fontsize=16, fontweight='bold')

ax.set_ylabel("Energy (eV)", fontsize=18, fontweight='bold')
ax.set_title("1T'-WTe2 Band Structure (PBE+SOC)", fontsize=20, fontweight='bold', pad=20)
ax.grid(True, which='major', linestyle='-', alpha=0.15, linewidth=1.5)

# Thicker borders
for spine in ax.spines.values():
    spine.set_linewidth(2)

import os
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "../figures/Fig1_BandStructure_Final.png")

plt.tight_layout()
plt.savefig(output_path, dpi=300)
print(f"Saved professional plot as {output_path}")
