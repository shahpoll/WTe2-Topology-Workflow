import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(16, 8)) # Slightly shorter height (16:9 -> 16:8)
ax.set_xlim(0, 12) 
ax.set_ylim(-1.5, 5.5) # Trimmed Y-limits
ax.axis('off')

# Function to draw box with text
def draw_step(x, y, text, script_name, color='#E3F2FD', edge_color='#1565C0', text_color='#01579B'):
    # Box - Massive
    rect = patches.FancyBboxPatch((x, y), 3.5, 1.8, boxstyle="round,pad=0.1", 
                                  linewidth=3.0, edgecolor=edge_color, facecolor=color)
    ax.add_patch(rect)
    
    # Text - "Hall Readable" Sizes
    # Title
    ax.text(x+1.75, y+1.1, text, ha='center', va='center', fontsize=22, fontweight='bold', color=text_color)
    # Subtext (Script)
    ax.text(x+1.75, y+0.5, f"{script_name}", ha='center', va='center', fontsize=16, 
            color='#37474F', fontweight='bold', fontfamily='monospace')

# --- DRAW STEPS (Adjusted Coordinates for Larger Boxes) ---
# 1. SCF
draw_step(0.5, 4, "DFT Ground State", "pw.x < scf", color='#E3F2FD', edge_color='#1E88E5')

# 2. NSCF
draw_step(4.5, 4, "Wavefunctions", "pw.x < nscf", color='#E3F2FD', edge_color='#1E88E5')

# 3. Projection
draw_step(8.5, 4, "Wannier Prep", "wannier90.x", color='#E3F2FD', edge_color='#1E88E5')

# 4. Minimization (Centered below NSCF/Prep)
draw_step(4.5, 1.5, "Minimization", "wannier90.x", color='#FFF3E0', edge_color='#FB8C00', text_color='#E65100')

# 5. Topology (Bottom)
draw_step(4.5, -0.8, "Topological Proof", "Python Scripts", color='#E8F5E9', edge_color='#43A047', text_color='#1B5E20')

# --- ARROWS (Thicker, adjusted for new positions) ---
style = "Simple, tail_width=4, head_width=15, head_length=15"
kw = dict(arrowstyle=style, color="#455A64", lw=3, ls='-')

# SCF -> NSCF
ax.add_patch(patches.FancyArrowPatch((4.0, 4.9), (4.5, 4.9), connectionstyle="arc3,rad=0", **kw))
# NSCF -> Prep
ax.add_patch(patches.FancyArrowPatch((8.0, 4.9), (8.5, 4.9), connectionstyle="arc3,rad=0", **kw))
# Prep -> Min (Curved back)
ax.add_patch(patches.FancyArrowPatch((10.25, 4.0), (8.0, 2.4), connectionstyle="arc3,rad=-0.4", **kw))
# Min -> Topology
ax.add_patch(patches.FancyArrowPatch((6.25, 1.5), (6.25, 1.0), connectionstyle="arc3,rad=0", **kw))

ax.set_title("Automation Pipeline: From DFT to Topology", fontsize=28, fontweight='bold', color='#263238', pad=30)
plt.tight_layout()
plt.savefig("Fig_Workflow.png", dpi=300, transparent=True)
print("Workflow flowchart generated (Enhanced).")
