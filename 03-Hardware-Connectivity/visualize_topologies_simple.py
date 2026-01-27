import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def visualize_topologies_simple(n_qubits=12):
    """
    Simple visualization of Linear vs All-to-All topologies without networkx.
    Avoids compatibility issues and renders directly.
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # --- 1. COMPETITOR: Linear Topology ---
    ax = axes[0]
    ax.set_xlim(-1, n_qubits)
    ax.set_ylim(-2, 2)

    # Draw nodes in a line
    for i in range(n_qubits):
        circle = patches.Circle((i, 0), 0.3, color='#FF6B6B', ec='#CC5555', linewidth=2)
        ax.add_patch(circle)
        ax.text(i, 0, str(i), ha='center', va='center', color='white', fontweight='bold', fontsize=8)

    # Draw edges (only nearest neighbors)
    for i in range(n_qubits - 1):
        ax.plot([i + 0.3, i + 0.7], [0, 0], color='gray', linewidth=2)

    ax.set_title("Competitor Architecture\n(Nearest Neighbor Only)", fontsize=14, fontweight='bold')
    ax.axis('off')

    # --- 2. IONQ: All-to-All Topology ---
    ax = axes[1]
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)

    # Draw nodes in a circle
    angles = np.linspace(0, 2 * np.pi, n_qubits, endpoint=False)
    positions = np.array([[np.cos(angle), np.sin(angle)] for angle in angles])

    # Draw edges (all-to-all) - thin and semi-transparent
    for i in range(n_qubits):
        for j in range(i + 1, n_qubits):
            x = [positions[i][0], positions[j][0]]
            y = [positions[i][1], positions[j][1]]
            ax.plot(x, y, color='#4D96FF', linewidth=0.5, alpha=0.2)

    # Draw nodes
    for i, (x, y) in enumerate(positions):
        circle = patches.Circle((x, y), 0.2, color='#4D96FF', ec='#2565CC', linewidth=2)
        ax.add_patch(circle)
        ax.text(x, y, str(i), ha='center', va='center', color='white', fontweight='bold', fontsize=7)

    ax.set_title("IonQ Architecture\n(All-to-All Connectivity)", fontsize=14, fontweight='bold')
    ax.axis('off')
    ax.set_aspect('equal')

    # Save
    plt.tight_layout()
    output_path = f"figures/topology_comparison_{n_qubits}qubits.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Visualization saved to: {output_path}")
    plt.close()

if __name__ == "__main__":
    visualize_topologies_simple(n_qubits=12)
