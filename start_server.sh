#!/bin/bash
# Startup script for Nepali RAG Flask Application (Linux/Mac)

echo "============================================"
echo "  Nepali RAG System - Flask Deployment"
echo "============================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "[INFO] Python found: $(python3 --version)"
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[INFO] Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment"
        exit 1
    fi
    echo "[SUCCESS] Virtual environment created"
    echo
fi

# Activate virtual environment
echo "[INFO] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment"
    exit 1
fi

# Install dependencies
echo "[INFO] Checking dependencies..."
if ! pip show flask &> /dev/null; then
    echo "[INFO] Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install dependencies"
        exit 1
    fi
    echo "[SUCCESS] Dependencies installed"
    echo
fi

# Check if FAISS index exists
echo "[INFO] Checking FAISS index..."
FAISS_PATH="/mnt/d/Nepali_RAG_Project/nepali_vectorstore_bgem3/index.faiss"
if [ ! -f "$FAISS_PATH" ]; then
    echo "[WARNING] FAISS index not found at expected location"
    echo "Please ensure the index exists"
    echo
fi

# Start Flask application
echo "============================================"
echo "  Starting Flask Server..."
echo "============================================"
echo
echo "[INFO] Server will start at http://localhost:5000"
echo "[INFO] Press Ctrl+C to stop the server"
echo

python app.py
