# Infrastructure Feasibility: The Memory Bottleneck

| Resource | Standard Node (16GB) | JARVIS GPU Node (High-Mem) |
| :--- | :--- | :--- |
| **CPU Cores** | 12 Cores | 40+ Cores |
| **RAM Available** | 16 GB | 64+ GB |
| **Wannier Step** | **FAILED** (Out of Memory) | **SUCCESS** (Converged) |
| **Dense K-Mesh** | Impossible ($12\times12$ limit) | Enabled ($40\times40$ mesh) |
| **Time to Result** | $\infty$ (Crashed) | ~15 Minutes |

**Verdict:** High-memory infrastructure was *mandatory* for the Z2 topological workflow due to the dense k-mesh requirements of Wannier90.
