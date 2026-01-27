from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import TwoLocal
from qiskit.transpiler import CouplingMap

def demo_chemistry_fidelity(n_qubits=4):
    """
    Demonstrates the advantage of IonQ's Native Gate Set (MS Gate)
    over standard CNOT decomposition for Chemistry Ansatzes (VQE).

    The key insight: Chemistry simulations require extreme fidelity.
    Every 2-qubit gate adds error. IonQ's native gates minimize gates.
    """
    print(f"--- 🧪 Chemistry Demo: Molecular Ansatz Efficiency (VQE) ---")
    print(f"Simulating a {n_qubits}-qubit molecule (e.g., Carbon Dioxide Fragment)...\n")

    # 1. Create a Chemistry "Ansatz"
    # This is the trial wavefunction we tune to find the molecule's ground state energy.
    # We use a 'TwoLocal' circuit, very common in VQE (Variational Quantum Eigensolver).
    # It consists of Rotation layers (single qubit) and Entanglement layers (two qubit).
    ansatz = TwoLocal(n_qubits, ['ry', 'rz'], 'cz', entanglement='full', reps=3)

    # 2. Define the Hardware Constraints

    # COMPETITOR: Standard Superconducting (Linear Topology + CNOT Basis)
    # They must use CNOT (cx) gates, often with multiple decomposition steps.
    competitor_basis = ['cx', 'rz', 'sx', 'x']
    competitor_map = CouplingMap.from_line(n_qubits)

    # IONQ: Trapped Ion (All-to-All + Native MS Basis)
    # IonQ's native entangling gate is the Mølmer–Sørensen (MS) gate.
    # In Qiskit, this is represented as 'rxx' (Ising coupling).
    ionq_basis = ['rxx', 'ry', 'rx']
    ionq_map = None  # All-to-All

    # 3. Compile (Transpile)
    print("[Compiling for COMPETITOR (Standard CNOT basis + Linear topology)]...")
    comp_circuit = transpile(ansatz,
                             coupling_map=competitor_map,
                             basis_gates=competitor_basis,
                             optimization_level=3)

    print("[Compiling for IONQ (Native MS/RXX basis + All-to-All topology)]...")
    ionq_circuit = transpile(ansatz,
                             coupling_map=ionq_map,
                             basis_gates=ionq_basis,
                             optimization_level=3)

    # 4. The "Fidelity" Report
    # In VQE, the killer metric is the "Two-Qubit Gate Count".
    # 2-qubit gates have 10x-100x more error than 1-qubit gates.
    # In chemistry, we care about "Chemical Accuracy" (~1.6 mHartree).
    # Too much error → fail to reach chemical accuracy.

    comp_ops = comp_circuit.count_ops()
    ionq_ops = ionq_circuit.count_ops()

    comp_2q_count = comp_ops.get('cx', 0)
    ionq_2q_count = ionq_ops.get('rxx', 0)

    comp_1q_count = sum([comp_ops.get(g, 0) for g in ['rx', 'ry', 'rz', 'sx', 'x']])
    ionq_1q_count = sum([ionq_ops.get(g, 0) for g in ['rx', 'ry', 'rz']])

    # Calculate Depth (Time for quantum decoherence to set in)
    comp_depth = comp_circuit.depth()
    ionq_depth = ionq_circuit.depth()

    print(f"\n--- 🔬 MOLECULAR SIMULATION EFFICIENCY REPORT ---")
    print(f"Ansatz: {n_qubits}-qubit VQE (Variational Quantum Eigensolver)")
    print(f"Target: Carbon Dioxide or Metal-Organic Framework Fragment\n")

    print(f"[Competitor (CNOT Basis + Linear Topology)]")
    print(f"  - 1-Qubit Gates: {comp_1q_count}")
    print(f"  - Critical 2-Qubit Gates: {comp_2q_count}")
    print(f"  - Total Circuit Depth: {comp_depth} layers")
    print(f"  - Error Accumulation: ~{comp_2q_count * 0.01:.1%} (assuming 1% per 2q-gate)")

    print(f"\n[IonQ (Native MS/RXX Basis + All-to-All Topology)]")
    print(f"  - 1-Qubit Gates: {ionq_1q_count}")
    print(f"  - Critical 2-Qubit Gates: {ionq_2q_count}")
    print(f"  - Total Circuit Depth: {ionq_depth} layers")
    print(f"  - Error Accumulation: ~{ionq_2q_count * 0.001:.1%} (assuming 0.1% per native gate)")

    # Improvement calculation
    gate_reduction = comp_2q_count - ionq_2q_count
    depth_ratio = comp_depth / ionq_depth if ionq_depth > 0 else float('inf')

    print(f"\n>>> ADVANTAGE: IonQ simulation uses {gate_reduction} fewer critical gates.")
    print(f">>> DEPTH RATIO: IonQ circuit is {depth_ratio:.1f}x shallower.")
    print(f"\n>>> WHY THIS MATTERS FOR CHEMISTRY:")
    print(f"    - Every 2-qubit gate introduces error (~1% for competitors, 0.1% for IonQ)")
    print(f"    - Chemistry requires 'Chemical Accuracy' (~1.6 mHartree tolerance)")
    print(f"    - Competitor: {comp_2q_count} errors multiply → Signal lost in noise")
    print(f"    - IonQ: {ionq_2q_count} errors → Clean, usable energy surface")
    print(f"\n>>> NATIVE GATE ADVANTAGE:")
    print(f"    - We aren't forcing the hardware to speak CNOT language")
    print(f"    - We speak IonQ's native language (Mølmer–Sørensen)")
    print(f"    - That's {gate_reduction} fewer 'translation errors'")

if __name__ == "__main__":
    # Try increasing qubits to see the advantage grow
    # n_qubits=4 → baseline
    # n_qubits=6 → noticeable advantage
    # n_qubits=8 → dramatic advantage (but takes longer to compile)
    demo_chemistry_fidelity(n_qubits=6)
