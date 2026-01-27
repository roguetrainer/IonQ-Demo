import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFT
from qiskit.transpiler import CouplingMap

def run_connectivity_challenge(n_qubits=10):
    """
    Demonstrates the difference in circuit depth/complexity between
    IonQ's All-to-All connectivity and a Standard Linear/Grid topology.
    """
    print(f"--- 🥊 Connectivity Challenge: {n_qubits} Qubits ---\n")

    # 1. Create a QFT Circuit (Requires heavy connectivity)
    #    QFT is the 'worst case scenario' for limited connectivity
    circuit = QFT(n_qubits)
    print(f"Original Circuit Operations: {circuit.count_ops()}")

    # 2. Define Topologies

    # COMPETITOR: Linear Chain (0-1-2-3...)
    # This represents many superconducting architectures where qubits only talk to neighbors.
    linear_map = CouplingMap.from_line(n_qubits)

    # IONQ: All-to-All
    # In Qiskit, passing coupling_map=None implies All-to-All connectivity.
    ionq_map = None

    # 3. Transpile (Compile) for the Architectures
    print("\n[Compiling for COMPETITOR (Linear Topology)...]")
    competitor_circuit = transpile(circuit,
                                   coupling_map=linear_map,
                                   optimization_level=3) # High optimization to be fair

    print("[Compiling for IONQ (All-to-All Topology)...]")
    ionq_circuit = transpile(circuit,
                             coupling_map=ionq_map,
                             optimization_level=3)

    # 4. Compare Results
    print("\n--- 🏆 RESULTS ---")

    # Count SWAP gates (The "Tax" paid for poor connectivity)
    comp_ops = competitor_circuit.count_ops()
    ionq_ops = ionq_circuit.count_ops()

    comp_swaps = comp_ops.get('swap', 0)
    ionq_swaps = ionq_ops.get('swap', 0)

    # Calculate Depth (Time to execute)
    comp_depth = competitor_circuit.depth()
    ionq_depth = ionq_circuit.depth()

    print(f"\nCOMPETITOR (Linear Chain):")
    print(f"  - Total Gates: {sum(comp_ops.values())}")
    print(f"  - SWAP Gates:  {comp_swaps} (Use this number in your pitch!)")
    print(f"  - Circuit Depth: {comp_depth}")

    print(f"\nIONQ (All-to-All):")
    print(f"  - Total Gates: {sum(ionq_ops.values())}")
    print(f"  - SWAP Gates:  {ionq_swaps}")
    print(f"  - Circuit Depth: {ionq_depth}")

    print(f"\n>>> IMPACT: The competitor circuit is {comp_depth/ionq_depth:.1f}x deeper.")
    if comp_swaps > 0:
        print(f">>> REASON: The competitor wasted {comp_swaps} gates just moving data around.")

# Run the demo
if __name__ == "__main__":
    run_connectivity_challenge(n_qubits=10) # Try changing to 5 or 15
