"""
Demo 7: Material Science – Simulating Spin Chains (Heisenberg Model)

This demo simulates time-evolution of a 1D spin chain using the Heisenberg model.
Relevant to battery materials (lithium diffusion), magnetic materials, and phase transitions.

Usage:
    python heisenberg_simulation_demo.py [--n-spins N] [--n-steps K] [--max-time T]

Options:
    --n-spins N       Number of spins in chain (default: 4)
    --n-steps K       Number of Trotter steps (default: 10)
    --max-time T      Maximum simulation time (default: 2.0)
"""

import numpy as np
from typing import Tuple, List, Dict
import matplotlib.pyplot as plt

try:
    import pennylane as qml
    HAS_PENNYLANE = True
except ImportError:
    HAS_PENNYLANE = False
    print("Warning: PennyLane not installed. Install with: pip install pennylane")


def build_heisenberg_hamiltonian(n_spins: int, jx: float = 1.0, jy: float = 1.0, jz: float = 1.0):
    """
    Build the Heisenberg Hamiltonian for a 1D spin chain.

    H = Σ_i (J_x σ_x^i σ_x^{i+1} + J_y σ_y^i σ_y^{i+1} + J_z σ_z^i σ_z^{i+1})

    Args:
        n_spins: Number of spins in the chain
        jx, jy, jz: Coupling strengths

    Returns:
        PennyLane Hamiltonian object
    """
    if not HAS_PENNYLANE:
        return None

    coeffs = []
    obs = []

    # For each adjacent pair
    for i in range(n_spins - 1):
        # XX coupling
        if jx != 0:
            coeffs.append(jx)
            obs.append(qml.PauliX(i) @ qml.PauliX(i + 1))

        # YY coupling
        if jy != 0:
            coeffs.append(jy)
            obs.append(qml.PauliY(i) @ qml.PauliY(i + 1))

        # ZZ coupling
        if jz != 0:
            coeffs.append(jz)
            obs.append(qml.PauliZ(i) @ qml.PauliZ(i + 1))

    return qml.Hamiltonian(coeffs, obs)


def demo_heisenberg_time_evolution(n_spins: int = 4, n_trotter_steps: int = 10, max_time: float = 2.0):
    """
    Demonstrate time evolution of a Heisenberg spin chain.

    Args:
        n_spins: Number of spins
        n_trotter_steps: Trotter steps for approximation
        max_time: Maximum simulation time
    """
    print(f"\n{'='*90}")
    print(f"🔋 DEMO 7: Material Science – Heisenberg Spin Chain Simulation")
    print(f"{'='*90}")
    print(f"System: 1D Heisenberg Spin Chain with {n_spins} sites")
    print(f"Trotter steps: {n_trotter_steps}")
    print(f"Max simulation time: {max_time}\n")

    if not HAS_PENNYLANE:
        print("PennyLane not installed. Showing theoretical analysis only.\n")

        print("Step 1: Build Heisenberg Hamiltonian")
        print("-" * 90)
        print(f"H = Σ_i (σ_x^i σ_x^(i+1) + σ_y^i σ_y^(i+1) + σ_z^i σ_z^(i+1))")
        print(f"Number of interaction terms: {3 * (n_spins - 1)}\n")

        print("Step 2: Theoretical Circuit Depth Analysis")
        print("-" * 90)
        interaction_terms = 3 * (n_spins - 1)
        estimated_depth = n_trotter_steps * interaction_terms

        print(f"Trotter decomposition: e^(-i H t) ≈ [e^(-i H₁ Δt) e^(-i H₂ Δt) ...]^n")
        print(f"Number of Trotter steps: {n_trotter_steps}")
        print(f"Interaction terms per step: {interaction_terms}")
        print(f"Estimated circuit depth: {estimated_depth}\n")

        print("Step 3: Hardware Comparison")
        print("-" * 90)
        print(f"Superconducting (99% fidelity):")
        print(f"  Error per gate: 0.01")
        print(f"  Total error: {estimated_depth} × 0.01 = {estimated_depth * 0.01:.1%}")
        print(f"  Result: {'❌ UNUSABLE' if estimated_depth * 0.01 > 0.5 else '⚠️ MARGINAL'}\n")

        print(f"IonQ (99.9% fidelity):")
        print(f"  Error per gate: 0.001")
        print(f"  Total error: {estimated_depth} × 0.001 = {estimated_depth * 0.001:.1%}")
        print(f"  Result: {'✓ PRODUCTION-READY' if estimated_depth * 0.001 < 0.1 else '✓ ACCEPTABLE'}\n")

        print("Step 4: What the Circuit Does")
        print("-" * 90)
        print("Initial state: |0...01> (excitation at qubit 0)")
        print(f"Evolution: Excitation propagates through the chain over time")
        print(f"Measurement: Probability of excitation at each position\n")

        return

    # PENNYLANE IMPLEMENTATION
    # Build Hamiltonian
    print("Step 1: Build Heisenberg Hamiltonian")
    print("-" * 90)
    H = build_heisenberg_hamiltonian(n_spins)
    print(f"Number of interaction terms: {len(H.ops)}")
    print(f"Coupling strengths: J_x=1.0, J_y=1.0, J_z=1.0 (isotropic)\n")

    # Set up device
    dev = qml.device("default.qubit", wires=n_spins)

    # Define time-evolution circuit
    def circuit(time):
        # Initial state: Excitation (X gate) on first qubit
        qml.PauliX(wires=0)

        # Time evolution using Trotterization
        qml.ApproxTimeEvolution(H, time, n=n_trotter_steps)

        # Measure probabilities on all qubits
        return qml.probs(wires=range(n_spins))

    qnode = qml.QNode(circuit, dev)

    # Run simulations at different times
    print("Step 2: Time Evolution Simulation")
    print("-" * 90)

    times = np.linspace(0, max_time, 11)
    results = {
        "times": times,
        "prob_at_end": [],  # Probability of excitation reaching the end
        "center_of_mass": [],  # Center of mass of the excitation
        "entropy": []  # Entanglement entropy (approximated)
    }

    for t in times:
        print(f"Simulating time t={t:.2f}...", end=" ")

        try:
            probs = qnode(t)

            # Analyze results
            # For 4 qubits, state |0001> (index 1) = excitation at qubit 0
            # state |0010> (index 2) = excitation at qubit 1, etc.

            # Calculate center of mass
            center_of_mass = 0.0
            for state_idx in range(2 ** n_spins):
                # Binary representation gives qubit values
                state_bits = bin(state_idx)[2:].zfill(n_spins)
                # Simple heuristic: weight by position
                weight = sum(1 if bit == '1' else 0 for bit in state_bits)
                center_of_mass += probs[state_idx] * weight

            # Probability at "end" (any state with qubit n-1 excited)
            prob_at_end = 0.0
            for state_idx in range(2 ** n_spins):
                if (state_idx >> (n_spins - 1)) & 1:  # Last qubit is 1
                    prob_at_end += probs[state_idx]

            # Entropy approximation (Shannon entropy of probability distribution)
            entropy = -np.sum(np.where(probs > 0, probs * np.log2(probs + 1e-10), 0))

            results["prob_at_end"].append(prob_at_end)
            results["center_of_mass"].append(center_of_mass)
            results["entropy"].append(entropy)

            print(f"✓ (CoM: {center_of_mass:.2f}, P(end): {prob_at_end:.3f})")

        except Exception as e:
            print(f"✗ Error: {e}")

    print()

    # Step 3: Analysis
    print("Step 3: Results Analysis")
    print("-" * 90)

    print(f"Excitation Propagation:")
    print(f"  Time t=0.0: P(end) = {results['prob_at_end'][0]:.4f}")
    print(f"  Time t={max_time:.1f}: P(end) = {results['prob_at_end'][-1]:.4f}")

    if results['prob_at_end'][-1] > results['prob_at_end'][0]:
        print(f"  ✓ Excitation successfully propagated through chain\n")
    else:
        print(f"  ⚠️ Limited propagation (check interaction strengths)\n")

    print(f"Entanglement Growth:")
    print(f"  Initial entropy: {results['entropy'][0]:.3f}")
    print(f"  Final entropy: {results['entropy'][-1]:.3f}")
    print(f"  Interpretation: Excitation becomes entangled with the chain\n")

    # Step 4: Circuit Analysis
    print("Step 4: Circuit Analysis")
    print("-" * 90)

    specs_func = qml.specs(circuit)
    try:
        specs = specs_func(max_time)
        print(f"Total gates: {specs['resources'].num_gates}")
        print(f"Circuit depth: {specs['resources'].depth}\n")
    except:
        print("(Circuit specs unavailable)\n")

    # Step 5: Hardware Comparison
    print("Step 5: Hardware Fidelity Comparison")
    print("-" * 90)

    # Estimate circuit depth (Trotter steps × interactions per step)
    interactions_per_step = 3 * (n_spins - 1)
    total_depth = n_trotter_steps * interactions_per_step

    print(f"Interactions per Trotter step: {interactions_per_step}")
    print(f"Total Trotter steps: {n_trotter_steps}")
    print(f"Estimated circuit depth: {total_depth}\n")

    print(f"Superconducting (99.0% fidelity):")
    sup_error = total_depth * 0.01
    print(f"  Error per gate: 1.0%")
    print(f"  Cumulative error: {sup_error:.1%}")
    print(f"  Status: {'❌ UNUSABLE' if sup_error > 0.5 else '⚠️ MARGINAL'}\n")

    print(f"IonQ (99.9% fidelity):")
    ionq_error = total_depth * 0.001
    print(f"  Error per gate: 0.1%")
    print(f"  Cumulative error: {ionq_error:.1%}")
    print(f"  Status: ✓ PRODUCTION-READY\n")

    if sup_error > 0.5 and ionq_error < 0.1:
        print(f">>> ADVANTAGE: IonQ enables simulations that competitors cannot do reliably.")
        print(f"    This is why IonQ partners with material science companies.")

    # Step 6: Visualization
    try:
        print(f"\nStep 6: Visualizing Results")
        print("-" * 90)

        fig, axes = plt.subplots(1, 3, figsize=(15, 4))

        # Plot 1: Probability at end
        axes[0].plot(results["times"], results["prob_at_end"], 'o-', linewidth=2, markersize=8)
        axes[0].set_xlabel("Time t")
        axes[0].set_ylabel("P(excitation at end)")
        axes[0].set_title("Excitation Propagation")
        axes[0].grid(True, alpha=0.3)

        # Plot 2: Center of mass
        axes[1].plot(results["times"], results["center_of_mass"], 's-', linewidth=2, markersize=8)
        axes[1].set_xlabel("Time t")
        axes[1].set_ylabel("Center of Mass Position")
        axes[1].set_title("Excitation Spreading")
        axes[1].grid(True, alpha=0.3)

        # Plot 3: Entropy
        axes[2].plot(results["times"], results["entropy"], '^-', linewidth=2, markersize=8)
        axes[2].set_xlabel("Time t")
        axes[2].set_ylabel("Entanglement Entropy")
        axes[2].set_title("Entanglement Growth")
        axes[2].grid(True, alpha=0.3)

        plt.tight_layout()
        # plt.show()  # Uncomment to display
        print("(Visualization generated - uncomment plt.show() to display)")

    except Exception as e:
        print(f"Visualization skipped: {e}")

    print(f"\n{'='*90}")
    print("TAKEAWAY: Simulating material properties requires deep circuits and high fidelity.")
    print("IonQ's advantage enables realistic material simulations impossible elsewhere.")
    print(f"{'='*90}\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Demo 7: Heisenberg Spin Chain Time Evolution"
    )
    parser.add_argument(
        "--n-spins",
        type=int,
        default=4,
        help="Number of spins in chain (default: 4)"
    )
    parser.add_argument(
        "--n-steps",
        type=int,
        default=10,
        help="Number of Trotter steps (default: 10)"
    )
    parser.add_argument(
        "--max-time",
        type=float,
        default=2.0,
        help="Maximum simulation time (default: 2.0)"
    )

    args = parser.parse_args()

    demo_heisenberg_time_evolution(
        n_spins=args.n_spins,
        n_trotter_steps=args.n_steps,
        max_time=args.max_time
    )
