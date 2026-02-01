@echo off
REM Startup script for Nepali RAG Flask Application
echo ============================================
echo   Nepali RAG System - Flask Deployment
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [INFO] Python found
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created
    echo.
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install dependencies
echo [INFO] Checking dependencies...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing dependencies from requirements.txt...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [SUCCESS] Dependencies installed
    echo.
)

REM Check if FAISS index exists
echo [INFO] Checking FAISS index...
if not exist "D:\Nepali_RAG_Project\nepali_vectorstore_bgem3\index.faiss" (
    echo [WARNING] FAISS index not found at expected location
    echo Please ensure the index exists at: D:\Nepali_RAG_Project\nepali_vectorstore_bgem3\
    echo.
    pause
)

REM Start Flask application
echo ============================================
echo   Starting Flask Server...
echo ============================================
echo.
echo [INFO] Server will start at http://localhost:5000
echo [INFO] Press Ctrl+C to stop the server
echo.

python app.py

pause
