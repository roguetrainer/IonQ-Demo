# Chemistry Demo: Carbon Capture Material Simulation (QC-AFQMC)

## Overview

This demo demonstrates how IonQ's high gate fidelity enables accurate quantum simulation of materials relevant to carbon capture—real-world science that matters for climate tech.

## The Business Problem

Simulating molecular systems requires extreme accuracy. Classical computers struggle with large molecules; quantum computers promise speedup, but only if gate fidelities are high enough to preserve "chemical accuracy."

## What This Demo Shows

**Quantum-Classical Auxiliary-Field Quantum Monte Carlo (QC-AFQMC)**

- Simulates ground state energy of carbon capture materials
- Example: metal-organic framework (MOF) fragments
- Real-world application: IonQ has demonstrated this with Hyundai

## Why IonQ Hardware Matters

### The Challenge

Chemistry simulations typically use VQE (Variational Quantum Eigensolver), which is extremely noise-sensitive. If your quantum hardware isn't accurate enough, you lose "chemical accuracy"—results become unreliable for practical materials science.

### Your Advantage with IonQ

Industry-leading gate fidelity unlocks real results:

- Typical single-qubit gate fidelity: >99.9% (often quoted as "three 9s")
- Far exceeds NISQ competitor capabilities
- Enables direct use of native gates (Mølmer–Sørensen) without decomposition
- Results in cleaner, more accurate energy surfaces than standard CNOT approaches

## Key Metrics to Demonstrate

- Ground state energy accuracy vs. classical reference
- Chemical accuracy threshold (typically ~1.6 mHartree)
- Gate fidelity comparison with competitors
- Energy surface smoothness (fewer outliers = more reliable)

## The Core Logic: Native Gates vs. CNOT Decomposition

Chemistry simulations use **Variational Quantum Eigensolver (VQE)** to find molecular ground state energy.

**The Challenge:**

- VQE requires many 2-qubit entangling gates
- Each 2-qubit gate has ~1% error on standard hardware (CNOT decompositions)
- Multiply by dozens of gates → noise accumulates → energy results become meaningless

**The IonQ Advantage:**

- IonQ's **Mølmer–Sørensen (MS) gate** is native—a single pulse operation
- No CNOT decomposition needed
- Error rate ~0.1% (10x better than standard 2-qubit gates)
- Result: Clean, accurate energy surface → Chemical accuracy achieved

## The "Two-Qubit Gate Tax"

When you show this demo, emphasize the **critical 2-qubit gate count**:

1. **Competitor hardware:** Needs 40+ CNOT gates per ansatz iteration
2. **IonQ:** Needs 20+ native MS gates
3. **Error multiplication:** 40 × 1% = 40% total error vs. 20 × 0.1% = 2% total error
4. **Result:** Competitor fails to reach chemical accuracy; IonQ succeeds

## Files in This Folder

- `chemistry_vqe_demo.py` – **Primary script** demonstrating VQE ansatz efficiency with native gates
- `README.md` – This file

## Running the Demo

```bash
python chemistry_vqe_demo.py
```

**Output:** 2-qubit gate count and circuit depth comparison between standard CNOT and IonQ native MS basis.

**Try these variations:**

- `demo_chemistry_fidelity(n_qubits=4)` – Baseline
- `demo_chemistry_fidelity(n_qubits=6)` – Noticeable advantage
- `demo_chemistry_fidelity(n_qubits=8)` – Dramatic advantage (slower to compile)

## Real-World Grounding

This work builds on IonQ's publicly announced collaboration with Hyundai on material science for carbon capture. This isn't theoretical—it's solving industry problems.

**What IonQ demonstrated:**
- Quantum simulation of atomic forces for MOF materials
- Accurate prediction of CO2 binding energies
- Performance impossible on standard quantum computers

## Enterprise Framework: Azure Quantum

Microsoft's **Azure Quantum** provides:
- Full VQE libraries compatible with IonQ hardware
- Resource estimators that show gate counts for different topologies
- Integration with IonQ backend

This proves enterprise readiness for production chemistry workflows.

---

## Disclaimer

This demonstration code is provided for educational and illustrative purposes only. The author has no affiliation with IonQ and is not authorized to speak on behalf of IonQ.

**Important Notes:**

- This code comes with **no guarantee of correctness** or fitness for any particular purpose
- The metrics, performance claims, and comparisons presented are **simulations only** and not based on empirical measurements from actual quantum hardware
- Results may vary significantly when running on real quantum devices due to noise, decoherence, and other practical limitations
- Users are responsible for validating any results independently before relying on them for decision-making
- The simulated "competitor" topology is a simplified model and may not accurately reflect real-world competing hardware performance

This code is provided under the MIT License. Use at your own risk.
