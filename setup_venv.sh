#!/bin/bash

# IonQ Demo - Virtual Environment Setup Script
# This script creates and activates a Python virtual environment for the IonQ demo

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}IonQ Demo - Virtual Environment Setup${NC}"
echo -e "${GREEN}========================================${NC}\n"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed.${NC}"
    echo "Please install Python 3.9 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${YELLOW}Python version: ${PYTHON_VERSION}${NC}"

# Define venv directory
VENV_DIR="venv"

# Create virtual environment
if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Virtual environment already exists at $VENV_DIR${NC}"
    read -p "Do you want to recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Removing existing virtual environment...${NC}"
        rm -rf "$VENV_DIR"
    else
        echo -e "${YELLOW}Using existing virtual environment.${NC}"
    fi
fi

# Create venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}✓ Virtual environment created${NC}\n"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"
echo -e "${GREEN}✓ Virtual environment activated${NC}\n"

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
python -m pip install --upgrade pip setuptools wheel -q
echo -e "${GREEN}✓ Pip upgraded${NC}\n"

# Install requirements
if [ -f "requirements.txt" ]; then
    echo -e "${YELLOW}Installing dependencies from requirements.txt...${NC}"
    pip install -r requirements.txt -q
    echo -e "${GREEN}✓ Dependencies installed${NC}\n"
else
    echo -e "${RED}Error: requirements.txt not found in current directory.${NC}"
    exit 1
fi

# Verify installation
echo -e "${YELLOW}Verifying installation...${NC}"
python -c "from qiskit import transpile; print('✓ Qiskit OK')" 2>/dev/null && echo "✓ All imports successful" || echo "⚠ Warning: Some imports may have failed"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}\n"

echo -e "${YELLOW}Next steps:${NC}"
echo "1. Verify the environment is active (you should see '(venv)' in your prompt)"
echo "2. Run the Jupyter notebook:"
echo -e "   ${GREEN}jupyter notebook IonQ_Demo_Notebook.ipynb${NC}"
echo ""
echo "3. Or run individual Python scripts:"
echo -e "   ${GREEN}python 03-Hardware-Connectivity/connectivity_challenge.py${NC}"
echo -e "   ${GREEN}python 01-Finance-AmericanOptions/finance_comparator_demo.py${NC}"
echo -e "   ${GREEN}python 02-Chemistry-CarbonCapture/chemistry_vqe_demo.py${NC}"
echo ""
echo "To deactivate the environment, run: deactivate"
echo ""
