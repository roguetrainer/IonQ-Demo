import networkx as nx
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid display issues
import matplotlib.pyplot as plt
import itertools

def visualize_topologies(n_qubits=10):
    """
    Generates side-by-side plots of a Standard Linear Topology vs. IonQ's All-to-All Topology.
    """
    # Create the figure
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # --- 1. COMPETITOR: Linear Topology (The Chain) ---
    G_linear = nx.Graph()
    G_linear.add_nodes_from(range(n_qubits))
    # Connect i to i+1
    linear_edges = [(i, i+1) for i in range(n_qubits-1)]
    G_linear.add_edges_from(linear_edges)

    pos_linear = nx.spring_layout(G_linear, seed=42) # Or simply a line layout
    # Force a straight line layout for maximum visual impact
    pos_linear = {i: (i, 0) for i in range(n_qubits)}

    nx.draw_networkx_nodes(G_linear, pos_linear, ax=axes[0], node_color='#FF6B6B', node_size=500)
    nx.draw_networkx_labels(G_linear, pos_linear, ax=axes[0], font_color='white')
    nx.draw_networkx_edges(G_linear, pos_linear, ax=axes[0], edge_color='gray', width=2)

    axes[0].set_title(f"Competitor Architecture\n(Nearest Neighbor Only)", fontsize=14, fontweight='bold')
    axes[0].set_axis_off()

    # --- 2. IONQ: All-to-All Topology (The Web) ---
    G_ionq = nx.Graph()
    G_ionq.add_nodes_from(range(n_qubits))
    # Connect every node to every other node
    all_edges = list(itertools.combinations(range(n_qubits), 2))
    G_ionq.add_edges_from(all_edges)

    # Circular layout highlights the 'everything touches everything' nature
    pos_ionq = nx.circular_layout(G_ionq)

    nx.draw_networkx_nodes(G_ionq, pos_ionq, ax=axes[1], node_color='#4D96FF', node_size=500)
    nx.draw_networkx_labels(G_ionq, pos_ionq, ax=axes[1], font_color='white')
    # Make edges semi-transparent so it doesn't look like a solid blob
    nx.draw_networkx_edges(G_ionq, pos_ionq, ax=axes[1], edge_color='#4D96FF', alpha=0.3, width=1.5)

    axes[1].set_title(f"IonQ Architecture\n(All-to-All Connectivity)", fontsize=14, fontweight='bold')
    axes[1].set_axis_off()

    # Save the plot
    plt.tight_layout()
    output_path = f"figures/topology_comparison_{n_qubits}qubits.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Visualization saved to: {output_path}")
    plt.close()

if __name__ == "__main__":
    visualize_topologies(n_qubits=12) # 12 is a good number to show the density difference
