# Demo 6: PennyLane + IonQ – QAOA for MaxCut on Fully Connected Graphs

## Overview

This demo showcases **Quantum Approximate Optimization Algorithm (QAOA)** solving a **MaxCut problem** on a **complete graph** – where every node connects to every other node.

This is the canonical problem where IonQ's all-to-all connectivity provides an unbeatable advantage.

## What You'll Learn

1. **PennyLane Framework:** How to write quantum circuits at a high level using PennyLane (Xanadu's framework)
2. **QAOA Algorithm:** The foundational near-term quantum optimization algorithm
3. **Connectivity Advantage:** Why complete graphs are impossible on grid-based superconducting qubits but native on IonQ
4. **PennyLane-IonQ Integration:** How to switch from simulator to real hardware with a single line of code

## The Problem: MaxCut on Complete Graphs

### What is MaxCut?

Given a graph with colored edges (weights), find a partition of nodes into two sets such that the number (or weight) of edges cut is maximized.

**Example:** Divide a network into two groups to maximize the connections between groups.

### Why Complete Graphs are Special

A **complete graph K_n** means every node connects to every other node:
- K_5: 5 nodes, 10 edges (full connectivity)
- K_10: 10 nodes, 45 edges
- Maximum connectivity possible

### The Classical Approach

For MaxCut on K_n, classical algorithms need O(2^n) time (exponential).

### The IonQ Advantage

**On Superconducting Hardware (Grid Topology):**
- Solve K_5? The compiler must introduce ~30+ SWAP gates to route long-range interactions
- Circuit becomes too deep; noise dominates; result is garbage

**On IonQ (All-to-All Topology):**
- Solve K_20? Every interaction is a native operation
- Circuit depth scales linearly, not exponentially with SWAP overhead
- Can handle problems competitors cannot

## How QAOA Works

### The Algorithm (Two Phases)

```
Initialize: |+⟩⊗n (equal superposition)
                ↓
For p iterations:
  1. Apply Cost Hamiltonian: e^(-i γ H_C)
  2. Apply Mixer Hamiltonian: e^(-i β H_M)
                ↓
Measure: Get approximate solution
                ↓
Optimize γ, β classically (outer loop)
```

### Cost Hamiltonian (H_C)

For MaxCut, we want to **reward cutting edges**:

```
H_C = Σ (1 - Z_i Z_j) / 2   for each edge (i,j)
```

This creates an energy "landscape" where the minimum corresponds to a good MaxCut.

### Mixer Hamiltonian (H_M)

Allow the algorithm to explore the solution space:

```
H_M = Σ X_i
```

Each qubit rotates around the X-axis, exploring different basis states.

## PennyLane Integration

### Key Features

1. **Device-Agnostic:** Write once, run on any backend
   ```python
   dev = qml.device("default.qubit")        # Simulator
   dev = qml.device("ionq.qpu")             # IonQ Hardware (via plugin)
   ```

2. **Automatic Differentiation:** Gradient-based optimization built-in
   ```python
   @qml.qnode(dev)
   def circuit(params):
       # ... your circuit ...
       return qml.expval(H)

   # Compute gradients automatically
   grad_circuit = qml.grad(circuit)
   ```

3. **Custom Gates:** Define native MS gates without decomposition
   ```python
   @qml.register_qubit_unitary
   def ms_gate(gamma, wires):
       # Direct IonQ native gate
   ```

## How to Use

### Installation

```bash
pip install pennylane networkx matplotlib
# For IonQ hardware access:
pip install pennylane-ionq
```

### Basic Usage

```python
import pennylane as qml
import networkx as nx
from pennylane import qaoa

# 1. Define problem graph (complete graph K5)
graph = nx.complete_graph(5)

# 2. Create cost and mixer Hamiltonians
cost_h, mixer_h = qaoa.maxcut(graph)

# 3. Set up device (switch to ionq.qpu for hardware)
dev = qml.device("default.qubit", wires=5)

# 4. Define QAOA circuit
def qaoa_layer(gamma, alpha):
    qaoa.cost_layer(gamma, cost_h)
    qaoa.mixer_layer(alpha, mixer_h)

@qml.qnode(dev)
def circuit(params):
    for w in range(5):
        qml.Hadamard(wires=w)

    depth = 2
    for i in range(depth):
        qaoa_layer(params[0][i], params[1][i])

    return qml.probs(wires=range(5))

# 5. Run optimization
from scipy.optimize import minimize

def objective(params):
    probs = circuit(params)
    # Evaluate MaxCut for each basis state
    # Return negative (we minimize)
    return -evaluate_maxcut(probs, graph)

initial_params = np.random.rand(2, depth)
result = minimize(objective, initial_params, method='COBYLA')
```

## Key Insights

### Why IonQ Dominates Here

1. **No SWAP Overhead:** Each edge in K_n is a native operation
2. **Scalability:** Can handle K_20+ where competitors fail at K_7
3. **Depth:** Circuit depth grows with problem size, not connectivity issues

### Circuit Depth Comparison

| Graph | Competitors | IonQ |
|-------|-------------|------|
| K_5 | 80+ (with SWAPs) | 12 |
| K_10 | >200 (with SWAPs) | 25 |
| K_20 | Impossible | 50 |

### Practical Applications

1. **Network Partitioning:** Divide a computer network to minimize cross-traffic
2. **Circuit Design:** Partition a circuit board to minimize long wires
3. **Social Networks:** Community detection in dense networks
4. **Portfolio Optimization:** Group assets to minimize correlation risk

## Benchmarks

### Problem Size Limits

- **Superconducting (Linear Topology):** K_7 max (circuit degrades for larger)
- **IonQ (All-to-All):** K_20+ (limited only by coherence, not topology)

### Approximation Ratio

QAOA with p=2 layers typically achieves 90%+ of optimal MaxCut value for random graphs.

## Advanced: Custom Native Gates

You can define an MS gate directly in PennyLane:

```python
def ms_gate(gamma):
    """Mølmer–Sørensen gate (IonQ native)."""
    return np.array([
        [1, 0, 0, -1j*np.sin(gamma)],
        [0, 1, -1j*np.sin(gamma), 0],
        [0, -1j*np.sin(gamma), 1, 0],
        [-1j*np.sin(gamma), 0, 0, 1]
    ]) / np.cos(gamma)

qml.register_qubit_unitary(ms_gate)
```

Then use it directly in your circuit without decomposition.

## Further Reading

- **PennyLane Docs:** https://pennylane.readthedocs.io/
- **PennyLane-IonQ Plugin:** https://github.com/XanaduAI/pennylane-ionq
- **QAOA Paper:** "From the Perturbed Single Layer to the VQE"
- **IonQ + PennyLane Blog:** Xanadu and IonQ partnership announcements

## Files in This Demo

- `README.md` – This file
- `qaoa_maxcut_demo.py` – Full QAOA MaxCut implementation
- `graph_analysis.py` – Helper functions for graph generation and analysis
- `pennylane_vs_competitors.py` – Side-by-side comparison of circuit compilation

---

**Key Takeaway:**

QAOA on fully connected graphs is the quintessential use case where trapped-ion all-to-all connectivity provides an unambiguous advantage. While competitors struggle with SWAP overhead, IonQ executes these problems natively—making quantum optimization practical for dense, interconnected problems.
