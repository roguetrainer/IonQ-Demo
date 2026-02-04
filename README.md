# Quantum Computing Demos on IonQ Hardware

These five demos showcase how IonQ's trapped-ion quantum computers solve real-world problems in your business. Each demo highlights specific capabilities—all-to-all connectivity, high gate fidelity, error mitigation, and circuit optimization—that directly impact your bottom line.

## Demo 1: Finance – American Option Pricing via Amplitude Estimation

**The Business Problem:** American options are computationally expensive because they can be exercised at any time. Pricing them requires sophisticated algorithms (like Longstaff-Schwartz) rather than simple closed-form solutions. This is where quantum computing provides a competitive advantage.

### What You'll Demonstrate

Implement a Quantum Amplitude Estimation (QAE) algorithm to accurately price American options by evaluating "stopping times" (exercise decision points) that are intractable on classical hardware.

### Why IonQ Hardware Matters for Your Business
**The Challenge:** Building arithmetic circuits to handle the "if-then" logic of option exercise requires many operations. On competitor hardware with limited connectivity, these operations demand massive overhead in data movement (SWAP gates), making circuits too slow and error-prone to be practical.

**Your Advantage with IonQ:** Our all-to-all connectivity lets you build compact, efficient arithmetic circuits without the movement overhead. This means faster convergence to the correct answer and reliable results your trading desk can depend on.

---

## Demo 2: Chemistry – Carbon Capture Material Simulation (QC-AFQMC)

**Real-World Relevance:** IonQ has publicly demonstrated this work with industry leaders like Hyundai. This isn't theoretical—it's solving actual material science challenges for carbon capture applications.

### What You'll Demonstrate

Simulate the ground state energy of a small, complex molecule relevant to carbon capture (like a metal-organic framework fragment) using QC-AFQMC (Quantum-Classical Auxiliary-Field Quantum Monte Carlo).

### Why IonQ Hardware Matters for Your Business

**The Challenge:** Chemistry simulations often use VQE (Variational Quantum Eigensolver), which is extremely sensitive to errors. If your quantum hardware isn't accurate enough, you lose "chemical accuracy"—the results become unreliable for practical use.

**Your Advantage with IonQ:** Our trapped-ion systems deliver industry-leading gate fidelity (often >99.9% for single-qubit operations), far exceeding competitor capabilities. Additionally, you can directly use IonQ's native gates (like the Mølmer–Sørensen gate) without decomposition, giving you cleaner, more accurate simulations right out of the box.

---

## Demo 3: Hardware Differentiator – The "Connectivity Challenge" (QFT or Graph Problems)

**The Business Case:** This demo gives you concrete, measurable proof of why IonQ's architecture is fundamentally superior to competitor hardware for certain classes of problems.

### What You'll Demonstrate

Run a Quantum Fourier Transform (QFT) or a MaxCut optimization on a fully connected graph—algorithms that inherently require every qubit to interact with every other qubit.

### Why IonQ Hardware Matters for Your Business

**The Technical Reality:** Algorithms like QFT need all-to-all qubit interactions.

- **With Competitor Hardware (Grid Topology):** Moving information between distant qubits requires a "bucket brigade" of SWAP gates, adding massive overhead and noise. The circuit becomes too deep to run reliably.
- **With IonQ:** You interact any qubit with any other directly in a single pulse. No overhead. No extra noise.

### How to Present It

1. Build a standard QFT circuit.
2. Compile it for a traditional grid topology (what your competitors use). Count the total gates—the SWAP overhead will be substantial.
3. Compile the same circuit for IonQ. Count the gates again—you'll see a dramatic reduction.
4. Run the IonQ version and show it converges to the correct answer reliably. Then explain that the competitor version would likely fail due to the accumulated noise from all those extra SWAPs.

---

## Demo 4: Error Mitigation – Debiasing & Sharpening

**The Business Impact:** Quantum algorithms that fail on raw hardware can be made production-ready through software-level error mitigation—no new quantum hardware needed.

**What You'll Demonstrate:** Use IonQ's Debiasing and Sharpening techniques to transform a noise-sensitive algorithm (Bernstein-Vazirani) from ~15% success rate to ~92% success rate.

**How It Works:**

- **Debiasing (Symmetrization):** Compiler generates 100+ circuit variants that systematically over-correct hardware errors. Averaging these variants cancels systematic biases while preserving the quantum signal.
- **Sharpening (Majority Voting):** For algorithms with known answer states, use plurality voting to recognize and boost the correct state, suppressing noise.

**Why This Matters:**

- Available TODAY on Azure Quantum and Amazon Braket
- No additional quantum hardware required—pure software optimization
- Can turn a "failed" experiment into useful results
- Direct leverage: Every IonQ customer can use this immediately

See [04-ErrorMitigation-Debiasing/](04-ErrorMitigation-Debiasing/) for full implementation and README.

---

## Demo 5: Circuit Compression – ZX Calculus for Trapped Ions

**The Business Impact:** Quantum circuits can be compressed by 75%+ by recognizing "Phase Gadgets" that are native to IonQ's Mølmer–Sørensen gates.

**What You'll Demonstrate:** Show how a chemistry circuit with 50 CNOT gates can be compressed to just 5 MS gates using ZX Calculus optimization—a 90% reduction in critical gates.

**How It Works:**

- **Phase Gadgets:** Common patterns in chemistry (CX-Rz-CX) that are inefficient with CNOTs but perfect for native MS gates
- **ZX Calculus:** A graphical representation where circuits become "spiders" (nodes) that can be fused
- **Compiler Magic:** ZX-aware compilation recognizes these patterns and maps them directly to native gates

**Why This Matters:**

- **Superconducting competitors:** Must decompose their CNOT basis to match the hardware—no further optimization possible
- **Trapped Ions (IonQ):** MS gates are symmetric and align perfectly with phase gadgets. ZX optimization collapses these patterns into single operations
- **Chemistry Advantage:** VQE and QAOA circuits are full of phase gadgets. This is why IonQ dominates chemistry simulations
- **Practical Result:** 4-5x shallower circuits → fewer errors → better results

See [05-Compilation-ZXCalculus/](05-Compilation-ZXCalculus/) for full implementation and README.

---

## Why These Five Demos Tell Your Story

When presenting to your stakeholders, your narrative should be: **"Quality over Quantity: The Complete Story."**

- **Demo 1 (Hardware):** All-to-all connectivity eliminates SWAP overhead—proving architectural superiority
- **Demo 2 (Finance):** Compact arithmetic circuits let you solve financial problems competitors cannot
- **Demo 3 (Chemistry):** Native gates and high fidelity unlock scientific breakthroughs
- **Demo 4 (Error Mitigation):** Software innovations bridge the gap to production-ready results
- **Demo 5 (Compilation):** ZX Calculus shows why trapped ions are the natural fit for chemistry and optimization

Together, they form a comprehensive narrative: **Physics (Architecture) + Software (Optimization) + Innovation (Error Mitigation) = Unmatched Performance.**

---

## Documentation

For strategic context and deeper physics understanding:

- [Docs/ROADMAP_AND_STRATEGY.md](Docs/ROADMAP_AND_STRATEGY.md) – The Oxford Ionics acquisition and future roadmap
- [Docs/PHYSICS_AND_GATES.md](Docs/PHYSICS_AND_GATES.md) – Deep dive into IonQ's native gates, ZX Calculus, and why trapped ions excel

---

## Next Steps

For the latest technical specifications and performance metrics to reference in your presentations, consult IonQ's technology updates and performance documentation.

---

## Disclaimer

This demonstration framework is provided for educational and illustrative purposes only. The author has no affiliation with IonQ and is not authorized to speak on behalf of IonQ.

**Important Notes:**

- This code comes with **no guarantee of correctness** or fitness for any particular purpose
- The metrics, performance claims, and comparisons presented are **simulations only** and not based on empirical measurements from actual quantum hardware
- Results may vary significantly when running on real quantum devices due to noise, decoherence, and other practical limitations
- Users are responsible for validating any results independently before relying on them for decision-making
- The simulated "competitor" topology is a simplified model and may not accurately reflect real-world competing hardware performance

This code is provided under the MIT License. Use at your own risk.
