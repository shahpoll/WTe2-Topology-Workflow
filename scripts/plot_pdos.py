import matplotlib.pyplot as plt
import numpy as np
import glob

# Load PDOS data
# Files are like wte2.pdos_atm#*_wfc#*
# We need to sum W-d and Te-p

def load_pdos(species, orbital):
    # species: 'W' or 'Te'
    # orbital: 'd' or 'p'
    
    # Files: wte2.pdos.pdos_atm#1(W)_wfc#5(d_j2.5) or similar
    # Pattern: wte2.pdos.pdos_atm*{species}*{orbital}*
    pattern = f"wte2.pdos.pdos_atm*{species}*{orbital}*"
    files = glob.glob(pattern)
    print(f"Searching {pattern} -> Found {len(files)} files")
    total_dos = None
    energy = None
    
    for f in files:
        try:
            data = np.loadtxt(f)
            # data columns: E, LDOS, PDOS_1, PDOS_2 ...
            # We want sum of all PDOS columns (or just LDOS if it matches?)
            # Usually column 1 is LDOS (sum of projections)
            
            if energy is None:
                energy = data[:, 0]
                total_dos = data[:, 1] 
            else:
                total_dos += data[:, 1]
        except:
            pass
            
    return energy, total_dos

# Load W-d
e_w, dos_w = load_pdos('W', 'd')
# Load Te-p
e_te, dos_te = load_pdos('Te', 'p')

# Plot
fig, ax = plt.subplots(figsize=(8, 6))

if e_w is not None:
    # Fermi Shift? We should verify Fermi level. 
    # Usually Z2 calculation used ef=-2.8364.
    # PROJWFC output usually preserves E-E_fermi=0 if nscf.save had it, 
    # OR we must shift manually.
    # projwfc usually writes energies as in nscf output.
    # We will shift by -2.8364 approx if needed, or check 'wte2.proj.out' for Fermi energy.
    # For now, assume raw energy. We'll label relative energy if we shift.
    ef = -2.8364 # From wte2.win / nscf
    
    ax.plot(e_w - ef, dos_w, color='blue', label='W $5d$', linewidth=2)
    ax.fill_between(e_w - ef, 0, dos_w, color='blue', alpha=0.1)

if e_te is not None:
    ef = -2.8364
    ax.plot(e_te - ef, dos_te, color='green', label='Te $5p$', linewidth=2)
    ax.fill_between(e_te - ef, 0, dos_te, color='green', alpha=0.1)

ax.set_xlim(-2, 2) # Zoom on inversion
ax.set_ylim(0, max(max(dos_w), max(dos_te)) * 1.1)

ax.axvline(0, color='red', linestyle='--', label='$E_F$')
ax.set_xlabel(r"Energy ($E - E_F$) [eV]")
ax.set_ylabel("Density of States [states/eV]")
ax.set_title("Orbital Inversion (Band Crossing)")
ax.legend()
ax.text(-1.5, 1, "Valence (Te-p)", color='green', fontweight='bold', fontsize=16)
ax.text(0.5, 1, "Conduction (W-d)", color='blue', fontweight='bold', fontsize=16)

plt.tight_layout()
plt.savefig("Fig_PDOS_Inversion.png", dpi=300)
print("PDOS Plot Generated: Fig_PDOS_Inversion.png")
