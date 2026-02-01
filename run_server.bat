@echo off
echo ============================================
echo   Starting Nepali RAG Server (Lazy Load)
echo ============================================
echo.
echo Server will start at: http://localhost:5000
echo Models will load on first query (be patient!)
echo Press Ctrl+C to stop
echo.
echo ============================================
echo.

cd /d D:\RAG_PROJECT_NEW
set HF_HUB_OFFLINE=1
set TRANSFORMERS_OFFLINE=1

python app_lazy.py

pause
