# Demo 4: The Noise Canceler – Error Mitigation with Debiasing & Sharpening

## Overview

This demo showcases IonQ's powerful **error mitigation** techniques: **Debiasing** (symmetrization) and **Sharpening** (majority voting). These techniques don't require new quantum algorithms—just a change in API flags—but the visual improvement in results is dramatic.

## What You'll Learn

1. **Systematic Errors:** How hardware biases (e.g., slightly-too-strong lasers) affect quantum results
2. **Debiasing:** Generating symmetric circuit variants to cancel systematic errors
3. **Sharpening:** Using majority voting to clean up noisy result distributions
4. **Practical Impact:** See a "broken" algorithm become usable with just software flags

## The Problem: Fragile Algorithms

Some quantum algorithms are noise-sensitive and produce poor results on real hardware:
- **Bernstein-Vazirani:** Requires perfect phase interference
- **Hidden Shift Problem:** Depends on quantum superposition staying coherent
- **Grover's Search:** Phase amplification breaks down with noise

On standard quantum hardware, these algorithms often fail due to systematic hardware errors.

## The Solution: IonQ's Symmetrization Compiler

### Debiasing: How It Works

1. **Identify systematic error:** Laser pulse slightly too strong → rotates +1° too far
2. **Generate variants:** Compiler creates 100+ circuit variations
   - Some variants flip the quantum logic (swap |0⟩ and |1⟩)
   - Some reverse rotation directions
   - Some use opposite phase shifts
3. **Average across variants:** Different variants "over-correct" the systematic error
4. **Result:** Averaging cancels the bias, preserves the quantum signal

### Sharpening: The Post-Processing Step

After debiasing, use **majority voting** on algorithms with known answer states:

1. **Recognize correct state:** If algorithm should output |0⟩, recognize this
2. **Compare variants:** Look at distribution of results across all debiasing variants
3. **Boost dominant state:** If 70% point to |0⟩, sharpen it to 95%
4. **Suppress noise:** Noise floor drops dramatically

## The Results

### Before Mitigation (Raw)

```
Result Distribution (1000 shots):
|00000⟩: 15%   ← Should be 100%, but systematic errors hurt us
|00001⟩: 12%
|00010⟩: 8%
... (lots of noise)
```

Success Rate: ~15% (unusable)

### After Debiasing

```
Result Distribution (across variants):
|00000⟩: 65%   ← Better, but still noisy
|00001⟩: 8%
|00010⟩: 5%
... (noise reduced)
```

Success Rate: ~65% (improving)

### After Sharpening

```
Result Distribution (sharpened):
|00000⟩: 92%   ← Clear, usable answer!
|00001⟩: 2%
|00010⟩: 1%
... (noise suppressed)
```

Success Rate: ~92% (production-ready)

## How to Use

### In Qiskit with IonQ Provider

```python
from qiskit import QuantumCircuit
from qiskit_ionq import IonQProvider, ErrorMitigation

# Create your circuit
qc = QuantumCircuit(n_qubits)
# ... build circuit ...

# Get backend
provider = IonQProvider()
backend = provider.get_backend("ionq_qpu")

# Run with Debiasing enabled
job_debiased = backend.run(
    qc,
    shots=1000,
    error_mitigation=ErrorMitigation.DEBIASING
)

# Retrieve results (Sharpening may be automatic or explicit)
result = job_debiased.result(sharpen=True)
counts = result.get_counts()
```

### Via Azure Quantum

In Azure Quantum's Jupyter notebook environment:
```python
backend.run(circuit, shots=1000, error_mitigation="debiasing")
```

Toggle in the Azure console to enable/disable for direct comparison.

### Via Amazon Braket

Through Amazon Braket's Python SDK:
```python
device.run(circuit, shots=1000, error_mitigation={"debiasing": True})
```

## Key Insights

### Why This Matters

1. **No new quantum algorithms:** Just software optimization
2. **Dramatic improvement:** Often 5-10x improvement in success rate
3. **Available today:** These are production features on Azure Quantum and Amazon Braket
4. **Transparent trade-off:** Uses extra shots (100 circuit variants) but dramatically improves signal quality

### Limitations

- **Assumes systematic errors are stationary:** Works well when hardware bias is consistent
- **Doesn't help with random errors:** Shot noise and temperature fluctuations still present
- **Requires multiple shots:** To average across variants
- **Not QEC:** Doesn't correct arbitrary quantum errors, just systematic biases

### When to Use

- **Use debiasing:** Any algorithm with noisy results
- **Add sharpening:** When the algorithm has a known, discrete answer (search, classification)
- **Don't need:** Simple algorithms that already work well (like preparing |0⟩)

## Real-World Application

### Carbon Capture (Hyundai Example)

Hyundai's carbon capture simulation using IonQ:
- **Without mitigation:** Results too noisy to be useful
- **With debiasing + sharpening:** Convergence becomes clear
- **Business impact:** Meaningful insights about molecular binding energies

This is exactly why error mitigation bridges the gap between "interesting quantum computer" and "useful quantum computer."

## Next Steps

1. Run `error_mitigation_demo.py` to see before/after results
2. Compare raw vs. debiased histograms visually
3. Experiment with the `n_qubits` and problem complexity
4. Try toggling debiasing on/off in the Azure console

## Files in This Demo

- `README.md` – This file
- `error_mitigation_demo.py` – Full implementation with side-by-side comparison
- `bernstein_vazirani.py` – Noise-sensitive Bernstein-Vazirani algorithm (helper)

## Further Reading

- IonQ Blog: "Error Mitigation on IonQ Hardware"
- Qiskit Documentation: ErrorMitigation module
- Azure Quantum: Error Mitigation Guide

---

**Key Takeaway:**

IonQ's error mitigation converts quantum computers from "interesting research devices" to "practical tools." The acquisition of Oxford Ionics will make this even more powerful as electronic control replaces lasers, reducing the systematic errors that debiasing corrects.
