import matplotlib.pyplot as plt
import os

# --- CONFIGURATION ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "../figures/Fig_Feasibility_Time.png")

def plot_time_feasibility():
    # Estimating CPU time based on typical scaling for SOC+Wannier calculations
    # Standard CPU (e.g., 4-8 cores): ~3-4 hours for full workflow
    # GPU Node: ~20 minutes (Your actual experience)
    times = [240, 20] # Minutes
    systems = ['Standard CPU Node\n(Est. 4 hours)', 'JARVIS GPU Node\n(~20 mins)']
    
    colors = ['gray', '#D50032']

    fig, ax = plt.subplots(figsize=(7, 5))
    
    bars = ax.bar(systems, times, color=colors, edgecolor='black', width=0.6)
    
    # Annotations
    ax.text(0, 245, "Slow Iteration Cycle", ha='center', va='bottom', color='gray', style='italic')
    ax.text(1, 25, "12x Speedup", ha='center', va='bottom', color='#D50032', fontweight='bold', fontsize=14)
    
    ax.set_ylabel("Time to Solution (Minutes)", fontsize=12)
    ax.set_title("Workflow Efficiency: CPU vs GPU", fontsize=14)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=300)
    print(f"Time feasibility chart saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    plot_time_feasibility()
