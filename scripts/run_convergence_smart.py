import os
import subprocess
import re
import time

# --- CONFIGURATION ---
# Smart Configuration:
# 1. Skip unstable low cutoffs (30, 40 Ry)
# 2. Focus on the physical regime (50, 60, 70, 80 Ry)
# 3. Use 60 Ry (Target) first to get a guaranteed result quickly
CUTOFFS = [60, 50, 70, 80] 

PSEUDO_DIR = "./" 
OUT_DIR = "convergence_results"
INPUT_TEMPLATE = "wte2.scf.in" 

def update_input(cutoff):
    with open(INPUT_TEMPLATE, 'r') as f:
        content = f.read()
    
    # Regex replace ecutwfc
    content = re.sub(r'ecutwfc\s*=\s*[\d\.]+', f'ecutwfc = {cutoff}', content)
    # Scale ecutrho 10x for safety (more stable than 8x for ultrasoft/PAW)
    content = re.sub(r'ecutrho\s*=\s*[\d\.]+', f'ecutrho = {cutoff*10}', content)
    
    filename = f"wte2_cut_{cutoff}.in"
    with open(filename, 'w') as f:
        f.write(content)
    return filename

def get_energy(outfile):
    try:
        # Grep the energy
        result = subprocess.check_output(f"grep ! {outfile}", shell=True).decode()
        return float(result.split('=')[1].split()[0])
    except:
        return None

def main():
    if not os.path.exists(OUT_DIR): os.makedirs(OUT_DIR)
    
    energies = []
    print("Starting SMART Convergence Study (Stable Regime)...")
    
    for cut in CUTOFFS:
        inp = update_input(cut)
        out = inp.replace(".in", ".out")
        
        print(f"Running Cutoff {cut} Ry (Priority High)...")
        # Run PW.x with MPI (4 cores)
        # Using nohup logic handled by caller, but internal execution is standard
        cmd = f"export OMPI_MCA_coll_hcoll_enable=0; mpirun -np 4 pw.x < {inp} > {OUT_DIR}/{out}"
        
        start_time = time.time()
        os.system(cmd)
        duration = time.time() - start_time
        
        E = get_energy(f"{OUT_DIR}/{out}")
        if E:
            energies.append(E)
            print(f"  -> Finished in {duration:.1f}s. Energy: {E} Ry")
        else:
            print("  -> Failed")
            energies.append(None)

    # Save Data
    valid_cuts = [c for c, e in zip(CUTOFFS, energies) if e is not None]
    valid_enes = [e for c, e in zip(CUTOFFS, energies) if e is not None]
    
    if valid_enes:
        # Sort for plotting (since we ran out of order)
        sorted_data = sorted(zip(valid_cuts, valid_enes))
        valid_cuts, valid_enes = zip(*sorted_data)
        
        # Delta Relative to 80 Ry (or max available)
        ref_E = valid_enes[-1]
        delta_E = [(e - ref_E)*13.605 for e in valid_enes] # eV
        
        with open(f"{OUT_DIR}/convergence_data_smart.txt", "w") as f:
            f.write("Cutoff(Ry) Energy(Ry) DeltaE(eV)\n")
            for c, e, de in zip(valid_cuts, valid_enes, delta_E):
                f.write(f"{c} {e} {de}\n")
        print(f"Data saved to {OUT_DIR}/convergence_data_smart.txt")
        
if __name__ == "__main__":
    main()
