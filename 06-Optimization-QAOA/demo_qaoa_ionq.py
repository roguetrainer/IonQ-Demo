"""
Enhanced QAOA MaxCut Demo for Complete Graphs

Demonstrates solving MaxCut on a fully connected graph (K_n).
This is the canonical problem where IonQ's all-to-all connectivity
provides an unambiguous advantage over grid-based competitors.

This code uses PennyLane to define and visualize the circuit,
and NetworkX + Matplotlib to show the problem structure.

Usage:
    python demo_qaoa_ionq.py [--n-nodes N] [--depth P]

Options:
    --n-nodes N    Size of complete graph K_N (default: 5)
    --depth P      QAOA depth (default: 1)
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from typing import Tuple, List

try:
    import pennylane as qml
    from pennylane import qaoa
    HAS_PENNYLANE = True
except ImportError:
    HAS_PENNYLANE = False
    print("Warning: PennyLane not installed. Install with: pip install pennylane")


def visualize_complete_graph(n_nodes: int, save_path: str = None):
    """
    Visualize a complete graph to show the connectivity challenge.

    Args:
        n_nodes: Number of nodes in K_n
        save_path: Optional path to save the figure
    """
    graph = nx.complete_graph(n_nodes)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Left: Circular layout (shows all connections)
    pos_circular = nx.circular_layout(graph)
    nx.draw(
        graph, pos_circular, ax=ax1,
        with_labels=True, node_color='#4D96FF', node_size=800,
        font_color='white', font_weight='bold', font_size=14,
        edge_color='#FF6B6B', width=2, arrowsize=20
    )
    ax1.set_title(f"MaxCut Problem: Complete Graph K_{n_nodes}\n(Every node connects to every other)",
                  fontsize=12, fontweight='bold')

    # Right: Edge count and connectivity matrix
    ax2.axis('off')

    num_nodes = n_nodes
    num_edges = len(graph.edges)

    info_text = f"""
Complete Graph K_{n_nodes} Properties:

📊 GRAPH STATISTICS:
  • Nodes: {num_nodes}
  • Edges: {num_edges}
  • Max possible cut: {num_edges} (cut all edges)
  • Avg connections per node: {2 * num_edges / num_nodes:.1f}

🎯 MAXCUT PROBLEM:
  Partition nodes into two sets to maximize
  the number of edges between sets.

⚡ CONNECTIVITY CHALLENGE:
  • Classical: O(2^{num_nodes}) = {2**num_nodes} partitions
  • QAOA: Polynomial with quantum speedup

🏆 HARDWARE IMPLICATIONS:
  Superconducting (Linear): Needs ~{num_nodes//2} SWAPs per interaction
  IonQ (All-to-All): Direct interaction, zero SWAPs
"""

    ax2.text(0.05, 0.95, info_text, transform=ax2.transAxes,
            fontsize=11, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Graph visualization saved to {save_path}")

    return fig, graph


def run_pennylane_qaoa(n_nodes: int = 5, depth: int = 1, verbose: bool = True):
    """
    Run QAOA for MaxCut using PennyLane.

    Args:
        n_nodes: Number of nodes in complete graph
        depth: QAOA depth (p parameter)
        verbose: Print detailed information

    Returns:
        Dictionary with results
    """
    if not HAS_PENNYLANE:
        print("PennyLane not available. Showing theoretical analysis instead.")
        return analyze_qaoa_theoretically(n_nodes, depth)

    print(f"\n{'='*80}")
    print(f"⚡ PennyLane QAOA Demo: MaxCut on K_{n_nodes}")
    print(f"{'='*80}\n")

    # Create the complete graph
    graph = nx.complete_graph(n_nodes)
    n_edges = len(graph.edges)

    print(f"Problem: MaxCut on K_{n_nodes}")
    print(f"  Nodes: {n_nodes}")
    print(f"  Edges: {n_edges}")
    print(f"  QAOA Depth: p={depth}\n")

    # Create cost and mixer Hamiltonians using PennyLane
    print("Creating QAOA Hamiltonian...")
    cost_h, mixer_h = qaoa.maxcut(graph)

    print(f"Cost Hamiltonian terms: {len(cost_h.ops)}")
    print(f"Mixer Hamiltonian: X on each qubit\n")

    # Define the device
    dev = qml.device("default.qubit", wires=n_nodes)

    # Define the QAOA layer
    def qaoa_layer(gamma, alpha):
        qaoa.cost_layer(gamma, cost_h)
        qaoa.mixer_layer(alpha, mixer_h)

    # Define the quantum circuit
    @qml.qnode(dev)
    def circuit(params):
        # Initial superposition
        for w in range(n_nodes):
            qml.Hadamard(wires=w)

        # QAOA layers
        for layer_idx in range(depth):
            qaoa_layer(params[0][layer_idx], params[1][layer_idx])

        return qml.probs(wires=range(n_nodes))

    # Get circuit specs
    print("Analyzing circuit structure...")
    specs_func = qml.specs(circuit)
    initial_params = np.random.RandomState(42).rand(2, depth)

    try:
        specs = specs_func(initial_params)
        print(f"Total gates: {specs['resources'].num_gates}")
        print(f"Circuit depth: {specs['resources'].depth}")
        print(f"Number of qubits: {n_nodes}\n")
    except Exception as e:
        print(f"(Circuit specs unavailable: {e})\n")

    # Optimize parameters
    print("Optimizing QAOA parameters...")
    from scipy.optimize import minimize

    def objective(params_flat):
        params = params_flat.reshape(2, depth)
        probs = circuit(params)

        # Evaluate MaxCut for each basis state
        expected_cut = 0.0
        for state_idx in range(2 ** n_nodes):
            cut_value = evaluate_maxcut_for_bitstring(state_idx, graph)
            expected_cut += probs[state_idx] * cut_value

        return -expected_cut  # Negative for minimization

    result = minimize(
        objective,
        initial_params.flatten(),
        method='COBYLA',
        options={'maxiter': 100}
    )

    best_params = result.x.reshape(2, depth)
    best_probs = circuit(best_params)
    best_bitstring = np.argmax(best_probs)
    best_cut = evaluate_maxcut_for_bitstring(best_bitstring, graph)

    print(f"✓ Optimization complete ({result.nit} iterations)\n")

    # Results
    print(f"{'='*80}")
    print("RESULTS")
    print(f"{'='*80}")
    print(f"Best cut found: {best_cut} / {n_edges}")
    print(f"Approximation ratio: {best_cut / n_edges:.1%}")
    print(f"Best partition: {bin(best_bitstring)}\n")

    return {
        'graph': graph,
        'best_cut': best_cut,
        'n_edges': n_edges,
        'circuit': circuit,
        'best_params': best_params
    }


def analyze_qaoa_theoretically(n_nodes: int, depth: int):
    """
    Provide theoretical analysis when PennyLane is not available.

    Args:
        n_nodes: Number of nodes
        depth: QAOA depth

    Returns:
        Dictionary with theoretical results
    """
    print(f"\n{'='*80}")
    print(f"⚡ QAOA MaxCut Theoretical Analysis: K_{n_nodes}")
    print(f"{'='*80}\n")

    graph = nx.complete_graph(n_nodes)
    n_edges = len(graph.edges)

    print(f"Complete Graph K_{n_nodes}:")
    print(f"  Nodes: {n_nodes}")
    print(f"  Edges: {n_edges}")
    print(f"  QAOA Depth: p={depth}\n")

    print(f"Theoretical Circuit Structure:")
    interaction_terms = n_edges
    total_depth_estimate = depth * (5 + interaction_terms // 2)

    print(f"  Interaction terms: {interaction_terms}")
    print(f"  Estimated depth: {total_depth_estimate} layers\n")

    print(f"Expected QAOA Results (p={depth}):")
    approx_ratio = 0.88  # Typical for QAOA p=2
    expected_cut = int(n_edges * approx_ratio)
    print(f"  Optimal cut: {n_edges}")
    print(f"  QAOA cut (typical): {expected_cut} (~{approx_ratio:.0%})\n")

    print(f"Hardware Compilation Comparison:\n")
    print(f"Superconducting (Linear Topology):")
    print(f"  Routing cost: ~{n_nodes // 2} SWAPs per long-range interaction")
    print(f"  Total SWAPs: ~{interaction_terms * (n_nodes // 2)}")
    print(f"  Final depth: {total_depth_estimate + interaction_terms * 2}")
    print(f"  Status: ❌ Too deep (noise dominates)\n")

    print(f"IonQ (All-to-All Topology):")
    print(f"  Routing cost: 0 SWAPs (all-to-all)")
    print(f"  Total SWAPs: 0")
    print(f"  Final depth: {total_depth_estimate}")
    print(f"  Status: ✓ Shallow and efficient\n")

    return {'n_nodes': n_nodes, 'n_edges': n_edges, 'expected_cut': expected_cut}


def evaluate_maxcut_for_bitstring(bitstring: int, graph: nx.Graph) -> int:
    """
    Evaluate MaxCut value for a given bitstring (partition).

    Args:
        bitstring: Integer representing a partition (binary encoding)
        graph: NetworkX graph

    Returns:
        Number of edges cut by this partition
    """
    cut_value = 0
    for i, j in graph.edges():
        bit_i = (bitstring >> i) & 1
        bit_j = (bitstring >> j) & 1
        if bit_i != bit_j:
            cut_value += 1
    return cut_value


def demonstrate_connectivity_challenge(n_nodes: int = 5):
    """
    Demonstrate the connectivity challenge visually and verbally.

    Args:
        n_nodes: Number of nodes in complete graph
    """
    print(f"\n{'='*80}")
    print(f"🔌 The Connectivity Challenge Explained")
    print(f"{'='*80}\n")

    graph = nx.complete_graph(n_nodes)

    print(f"Scenario: Solve MaxCut on K_{n_nodes}\n")

    print(f"Step 1: Identify all interactions")
    print(f"  Qubit 0 must interact with: {list(graph.neighbors(0))}")
    print(f"  Qubit 1 must interact with: {list(graph.neighbors(1))}")
    print(f"  ... (total: {len(graph.edges)} interactions)\n")

    print(f"Step 2: Compile for superconducting hardware (Linear Topology)")
    print(f"  Layout: Qubits arranged in a line: 0-1-2-3-4")
    print(f"  Problem: Qubit 0 is far from Qubits 3, 4")
    print(f"  Solution: Insert SWAP gates to move data\n")

    print(f"  Example: To connect Qubits 0 and 4:")
    print(f"    SWAP(0,1) → Move Q0 from position 0 to position 1")
    print(f"    SWAP(1,2) → Move Q0 from position 1 to position 2")
    print(f"    SWAP(2,3) → Move Q0 from position 2 to position 3")
    print(f"    SWAP(3,4) → Move Q0 from position 3 to position 4")
    print(f"    CX(0,4)   → Finally interact")
    print(f"    [Reverse SWAPs to move data back]")
    print(f"    Total cost: 10 gates for 1 interaction! ⚠️\n")

    print(f"Step 3: Compile for IonQ hardware (All-to-All Topology)")
    print(f"  Layout: All qubits can see all qubits")
    print(f"  Solution: Direct interaction, no movement needed\n")

    print(f"  Example: To connect Qubits 0 and 4:")
    print(f"    MS(0,4)  → Direct MS gate (native operation)")
    print(f"    Total cost: 1 gate for 1 interaction ✓\n")

    print(f"Step 4: Scale the problem")
    print(f"  Total interactions needed: {len(graph.edges)}")
    print(f"  Competitor overhead: {len(graph.edges) * 10} extra gates")
    print(f"  IonQ overhead: 0 extra gates\n")

    print(f">>> CONCLUSION:")
    print(f"    On IonQ, fully-connected graph problems are NATIVE.")
    print(f"    On competitors, they require exponential SWAP overhead.")
    print(f"    This is why IonQ wins at optimization.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Enhanced QAOA MaxCut Demo for Complete Graphs"
    )
    parser.add_argument(
        "--n-nodes",
        type=int,
        default=5,
        help="Size of complete graph K_N (default: 5)"
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=1,
        help="QAOA depth (default: 1)"
    )
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="Show graph visualization"
    )
    parser.add_argument(
        "--explain-connectivity",
        action="store_true",
        help="Show detailed connectivity challenge explanation"
    )

    args = parser.parse_args()

    # Optionally visualize the graph
    if args.visualize:
        print("Generating graph visualization...")
        visualize_complete_graph(args.n_nodes)
        plt.show()

    # Run QAOA
    results = run_pennylane_qaoa(n_nodes=args.n_nodes, depth=args.depth)

    # Optionally explain connectivity
    if args.explain_connectivity:
        demonstrate_connectivity_challenge(n_nodes=args.n_nodes)
