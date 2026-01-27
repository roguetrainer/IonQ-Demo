# IonQ Demo – Setup & Installation Guide

## Quick Start

### On macOS/Linux

```bash
cd IonQ-Demo
chmod +x setup_venv.sh
./setup_venv.sh
```

### On Windows

```cmd
cd IonQ-Demo
setup_venv.bat
```

That's it! The script will:
1. Check Python installation
2. Create a virtual environment
3. Install all dependencies
4. Verify the setup

---

## What Gets Installed

The setup creates an isolated Python environment with:

- **Qiskit** (0.43.0) – Quantum circuit library
- **Qiskit-Aer** – High-performance quantum simulator
- **NumPy, Matplotlib, NetworkX** – Scientific computing
- **Jupyter** – Interactive notebooks
- **Pandas, SciPy** – Data analysis & algorithms

See `requirements.txt` for exact versions.

---

## Manual Setup (Alternative)

If you prefer to set up manually:

### 1. Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 2. Upgrade Pip

```bash
python -m pip install --upgrade pip setuptools wheel
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
python -c "from qiskit import transpile; print('✓ Qiskit OK')"
```

---

## Running the Demos

### Option 1: Jupyter Notebook (Recommended for Presentations)

```bash
jupyter notebook IonQ_Demo_Notebook.ipynb
```

This opens the interactive notebook with all three demos. Run cells sequentially to see the output.

### Option 2: Individual Python Scripts

**Hardware Demo:**
```bash
python 03-Hardware-Connectivity/connectivity_challenge.py
```

**Finance Demo:**
```bash
python 01-Finance-AmericanOptions/finance_comparator_demo.py
```

**Chemistry Demo:**
```bash
python 02-Chemistry-CarbonCapture/chemistry_vqe_demo.py
```

### Option 3: Command-Line Testing

Test that everything works:

```bash
python -c "
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFT
from qiskit.transpiler import CouplingMap

# Quick test
circuit = QFT(5)
linear_map = CouplingMap.from_line(5)
result = transpile(circuit, coupling_map=linear_map, optimization_level=3)
print(f'✓ Setup verified! Circuit depth: {result.depth()}')
"
```

---

## Environment Variables (Optional)

If you have IonQ hardware access via Azure Quantum or AWS Braket:

```bash
# Set your IonQ credentials (not needed for simulation)
export IONQ_API_KEY="your-api-key"
export IONQ_WORKSPACE="your-workspace"
```

For cloud access, follow the official docs:
- **Azure Quantum:** https://azure.microsoft.com/en-us/services/quantum/
- **Amazon Braket:** https://aws.amazon.com/braket/

---

## Troubleshooting

### "Python command not found"

**macOS:** `python3` instead of `python`
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:** Ensure Python is in PATH. Download from https://www.python.org/

### "pip install fails"

Make sure your virtual environment is **activated**:

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```cmd
venv\Scripts\activate
```

You should see `(venv)` in your prompt.

### "Qiskit import error"

Reinstall Qiskit:
```bash
pip install --upgrade qiskit qiskit-aer
```

### "Jupyter not found"

Make sure you activated the venv and installed jupyter:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install jupyter
jupyter notebook
```

### "Permission denied" on setup_venv.sh

Make script executable:
```bash
chmod +x setup_venv.sh
./setup_venv.sh
```

---

## System Requirements

- **Python:** 3.9 or higher
- **RAM:** 4GB minimum (8GB+ recommended for larger demos)
- **Disk:** ~500MB for dependencies
- **Internet:** Required for initial package installation

---

## Deactivating the Environment

When you're done:

```bash
deactivate
```

This returns you to your system Python. The virtual environment files remain in `venv/` directory.

---

## Updating Dependencies

To update all packages to latest versions:

```bash
pip install --upgrade -r requirements.txt
```

To update a specific package:

```bash
pip install --upgrade qiskit
```

---

## Next Steps

1. ✅ Run setup script
2. 📓 Open Jupyter notebook: `jupyter notebook IonQ_Demo_Notebook.ipynb`
3. 🚀 Run the demos
4. 📊 Check the cheat sheet for presentation talking points: `PRESENTER_CHEAT_SHEET.md`
5. 🎤 Present to stakeholders!

---

## Support & Resources

- **Qiskit Docs:** https://qiskit.org/documentation/
- **IonQ Hardware:** https://ionq.com
- **Azure Quantum:** https://azure.microsoft.com/en-us/services/quantum/
- **Amazon Braket:** https://aws.amazon.com/braket/

---

**Created:** IonQ Demo Framework
**Version:** 1.0
**Last Updated:** 2026-01-26
