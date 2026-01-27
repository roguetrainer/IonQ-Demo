# Finance Demo: American Option Pricing via Amplitude Estimation

## Overview

This demo showcases how IonQ's all-to-all connectivity enables efficient quantum algorithms for financial derivatives pricing—specifically American options, which are computationally expensive on classical hardware.

## The Business Problem

American options can be exercised at any time before expiration, requiring sophisticated backwards induction methods (like Longstaff-Schwartz) to price accurately. Classical Monte Carlo approaches are slow; quantum amplitude estimation offers a potential speedup.

## What This Demo Shows

**Quantum Amplitude Estimation (QAE) Algorithm**

- Estimates the payoff of an American option
- Handles "stopping times" (exercise decision points) that are intractable on classical computers
- Requires arithmetic circuits (adders, comparators) for exercise condition logic

## Why IonQ Hardware Matters

### The Challenge

Building arithmetic circuits for "if-then" logic requires many operations. On competitor hardware with nearest-neighbor connectivity (grid topology), these operations demand massive SWAP gate overhead, making circuits too deep and noisy to be practical.

### Your Advantage with IonQ

All-to-all connectivity eliminates SWAP chains:

- Perform multi-qubit gates between any qubits directly
- Dramatically reduce circuit depth
- Achieve reliable results that competitors cannot

## Key Metrics to Demonstrate

- Gate count comparison: IonQ circuit vs. simulated grid topology
- Circuit depth reduction
- Convergence to correct option price
- Reliability/fidelity of results

## The Core Logic: The Comparator

American option pricing requires checking at each time step: **"Is Stock Price > Strike Price?"**

This is an **Integer Comparator** circuit—an arithmetic operation that requires many qubits to interact.

**On Competitor Hardware:**

- Stock price qubits must "hop" to reach strike price qubits
- Each hop = SWAP gate
- Deep, noisy circuit

**On IonQ:**

- Direct interaction between any qubits
- Compact, clean circuit
- Can execute 10+ times (one per time step) and still get clean results

## The "Multiplication of Error" Narrative

When presenting, emphasize this key insight:

1. **One comparator step** is expensive on competitor hardware
2. **American options require 10+ comparator steps** (one per time point)
3. **Competitor hardware:** Error multiplies → Result becomes noise
4. **IonQ:** Compact circuits stay clean even after 10+ iterations

## Files in This Folder

- `finance_comparator_demo.py` – **Primary script** that demonstrates the comparator efficiency
- `README.md` – This file

## Running the Demo

```bash
python finance_comparator_demo.py
```

**Output:** Gate count and circuit depth comparison between competitor and IonQ topologies.

**Try these variations:**

- `demo_finance_logic(num_state_qubits=4, value_to_compare=5)` – Small difference
- `demo_finance_logic(num_state_qubits=5, value_to_compare=11)` – Significant advantage
- `demo_finance_logic(num_state_qubits=6, value_to_compare=20)` – Dramatic advantage

## Enterprise Grounding: Microsoft Q#

**For a deeper technical dive:**

- Microsoft has `Microsoft.Quantum.Finance` library in Q#
- Pre-built function: `EstimateOptionPrice`
- Use **Azure Quantum Resource Estimator** to toggle "Qubit Connectivity" parameter
- This proves enterprise support for quantum finance workflows

**But for a live demo:** The Python script above is faster and more interactive than setting up Q# environment.
