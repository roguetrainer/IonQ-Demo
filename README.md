# Quantum Computing Demos on IonQ Hardware

These three demos showcase how IonQ's trapped-ion quantum computers solve real-world problems in your business. Each demo highlights specific capabilities—all-to-all connectivity and high gate fidelity—that directly impact your bottom line.

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

## Why These Three Demos Tell Your Story

When presenting to your stakeholders, your narrative should be: **"Quality over Quantity."**

- **Finance Demo** shows how connectivity lets you build complex financial algorithms that competitors simply cannot execute reliably.
- **Chemistry Demo** shows how precision (fidelity) unlocks real-world scientific breakthroughs that require accuracy.
- **Hardware Demo** gives you the hard numbers—gates counted, circuits compiled, results verified—that prove IonQ's architectural advantage.

---

## Next Steps

For the latest technical specifications and performance metrics to reference in your presentations, consult IonQ's technology updates and performance documentation.
