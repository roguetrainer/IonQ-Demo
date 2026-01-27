from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import IntegerComparator
from qiskit.transpiler import CouplingMap

def demo_finance_logic(num_state_qubits=4, value_to_compare=5):
    """
    Demonstrates the compilation efficiency of a Financial 'Comparator' circuit
    on IonQ vs. a Standard Linear Superconducting architecture.

    The comparator is the core logic step in American option pricing:
    "Is the current stock price > strike price? If yes, exercise the option."
    """
    print(f"--- 💰 Finance Demo: American Option Logic (Comparator) ---")
    print(f"Checking if a {num_state_qubits}-qubit Stock Price > {value_to_compare}...\n")

    # 1. The Financial Component: Integer Comparator
    # This circuit flips a target qubit if the input register >= value_to_compare
    # This is the core logic step in checking "Is the option in the money?"
    cmp_circuit = IntegerComparator(num_state_qubits=num_state_qubits, value=value_to_compare)

    # We measure the 'result' qubit (the flag that says "Yes, exercise option")
    cmp_circuit.measure_all()

    # 2. Define Hardware Topologies

    # COMPETITOR: Linear Chain (Standard Superconducting)
    # The control qubits must 'hop' down the line to reach the target.
    # We simulate a chain of appropriate length.
    linear_map = CouplingMap.from_line(cmp_circuit.num_qubits)

    # IONQ: All-to-All
    ionq_map = None # Implies fully connected

    # 3. Compile (Transpile)
    print("Compiling logic for [Competitor: Linear Chain]...")
    linear_transpiled = transpile(cmp_circuit, coupling_map=linear_map, optimization_level=3)

    print("Compiling logic for [IonQ: All-to-All]...")
    ionq_transpiled = transpile(cmp_circuit, coupling_map=ionq_map, optimization_level=3)

    # 4. The "Financial Advantage" Report
    linear_depth = linear_transpiled.depth()
    ionq_depth = ionq_transpiled.depth()

    linear_ops = linear_transpiled.count_ops()
    ionq_ops = ionq_transpiled.count_ops()

    linear_total_gates = sum(linear_ops.values())
    ionq_total_gates = sum(ionq_ops.values())

    print("\n--- 📊 OPTION PRICING EFFICIENCY REPORT ---")
    print(f"Logic: Compare {num_state_qubits}-qubit Register vs. Strike Price of {value_to_compare}")

    print(f"\n[Competitor (Linear Topology)]")
    print(f"  - Total Gates: {linear_total_gates}")
    print(f"  - Circuit Depth: {linear_depth}")
    print(f"  - SWAP Gates: {linear_ops.get('swap', 0)}")

    print(f"\n[IonQ (All-to-All Topology)]")
    print(f"  - Total Gates: {ionq_total_gates}")
    print(f"  - Circuit Depth: {ionq_depth}")
    print(f"  - SWAP Gates: {ionq_ops.get('swap', 0)}")

    if ionq_depth > 0:
        depth_ratio = linear_depth / ionq_depth
        print(f"\n>>> ADVANTAGE: IonQ is {depth_ratio:.1f}x shallower than competitor hardware.")

    gate_saved = linear_total_gates - ionq_total_gates
    print(f">>> GATES SAVED: {gate_saved} fewer operations on IonQ.")

    print("\n--- 💡 WHY THIS MATTERS FOR OPTION PRICING ---")
    print("In American options, this logic must run at EVERY time step.")
    print("If one step is expensive, a 10-step path becomes impossible on linear hardware.")
    print("On IonQ, you can afford to run this logic 10+ times and still get a clean answer.")

if __name__ == "__main__":
    # Try increasing qubits to see the gap widen
    # num_state_qubits=4 → small difference
    # num_state_qubits=5 or 6 → significant advantage
    demo_finance_logic(num_state_qubits=5, value_to_compare=11)
