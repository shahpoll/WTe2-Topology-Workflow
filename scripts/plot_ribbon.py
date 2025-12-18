import numpy as np
import matplotlib.pyplot as plt
import sys

# --- CONFIGURATION ---
WIDTH = 30        # Width of ribbon (unit cells).
NK = 150          # K-points along the periodic direction
FNAME = 'wte2_hr.dat'

def load_hr_dat(fname):
    """Parses standard Wannier90 hr.dat format."""
    try:
        with open(fname, 'r') as f:
            f.readline() # Time
            num_wann = int(f.readline())
            nrpts = int(f.readline())
            
            deg = []
            while len(deg) < nrpts:
                deg.extend(map(int, f.readline().split()))
                
            lines = f.readlines()
            all_nums = []
            for l in lines:
                all_nums.extend(l.split())
                
            iterator = iter(all_nums)
            hopping_dict = {} 
            
            # Total matrix elements expected
            total_elems = nrpts * num_wann * num_wann
            
            for _ in range(total_elems):
                rx = int(next(iterator))
                ry = int(next(iterator))
                rz = int(next(iterator))
                m  = int(next(iterator))
                n  = int(next(iterator))
                re = float(next(iterator))
                im = float(next(iterator))
                
                # Only 2D (Rz=0) needed, or keep all
                if rz == 0:
                    key = (rx, ry)
                    if key not in hopping_dict:
                        hopping_dict[key] = np.zeros((num_wann, num_wann), dtype=complex)
                    
                    # 1-based indexing in file -> 0-based in array
                    hopping_dict[key][m-1, n-1] = re + 1j*im 
                        
        return num_wann, hopping_dict
                        
        return num_wann, hopping_dict
    except FileNotFoundError:
        print(f"Error: {fname} not found.")
        sys.exit()

# --- MAIN CALCULATION ---
num_orb, hops = load_hr_dat(FNAME)
print(f"Hamiltonian Loaded. Orbitals: {num_orb}")

k_vals = np.linspace(0, 1.0, NK)
bands = []

print("Diagonalizing Slab Hamiltonian...")
for k_linear in k_vals:
    kx = k_linear * 2 * np.pi
    
    # Supercell Hamiltonian (Size: WIDTH * num_orb)
    H_slab = np.zeros((WIDTH*num_orb, WIDTH*num_orb), dtype=complex)
    
    for y_cell in range(WIDTH):
        for (rx, ry), mat_local in hops.items():
            # Phase for periodic direction (x)
            phase = np.exp(1j * kx * rx)
            
            # Target Y
            y_target = y_cell + ry
            
            if 0 <= y_target < WIDTH:
                row = y_cell * num_orb
                col = y_target * num_orb
                H_slab[row:row+num_orb, col:col+num_orb] += mat_local * phase
    
    evals = np.linalg.eigvalsh(H_slab)
    bands.append(evals)

bands = np.array(bands)

# --- PLOTTING ---
# Using landscape-ish or square-ish figure but focused
plt.figure(figsize=(6, 6))

# --- PLOTTING LOGIC ---
# 1. Plot ALL bands as "Bulk Continuum"
# User requested: "dimmed black lines arent much visible, swap it with other colours"
# We use a nice visible blue/slate color
for b in range(bands.shape[1]):
    plt.plot(k_vals, bands[:, b], color='#4682B4', alpha=0.3, linewidth=1.0, zorder=1) # SteelBlue

# 2. Identify and highlight Edge States (Red)
# Heuristic: Crosses zero gap
mid_k_idx = NK // 2
for b in range(bands.shape[1]):
    band_vals = bands[:, b]
    if min(band_vals) < 0 < max(band_vals):
        if abs(band_vals[mid_k_idx]) < 0.15: 
            plt.plot(k_vals, band_vals, color='#D50032', alpha=0.9, linewidth=2.5, zorder=2)

# Formatting - FOCUSED ZOOM
plt.ylim(-0.3, 0.3)
plt.xlim(0.2, 0.8) # Focus heavily on the crossing point (usually 0.5)
plt.axhline(0, color='black', linestyle=':', linewidth=1)
plt.xlabel(r"$k_{x}$ (Periodic Direction)")
plt.ylabel("Energy (eV)")
plt.title(f"Topological Edge States (Zoomed)")

plt.tight_layout()
plt.savefig("Fig_Ribbon_EdgeStates.png", dpi=300)
print("Ribbon calculation complete (Standard Colors, Zoomed).")
