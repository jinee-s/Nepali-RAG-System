"""
Configuration file for Nepali RAG System
Store sensitive information in environment variables
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Model Configuration
MODEL_NAME = "BAAI/bge-m3"
EMBEDDING_DIMENSION = 1024

# FAISS Configuration
FAISS_DIR = r"D:\Nepali_RAG_Project\nepali_vectorstore_bgem3"
INDEX_FILE = "index.faiss"
METADATA_FILE = "texts_only.pkl"

# API Keys (Load from environment variables in production)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyDS1OujZOOCJRLZOxiNqYxOe9Fqu9Ujhc0")

# Gemini Model
GEMINI_MODEL = "gemini-2.0-flash-exp"

# Retrieval Configuration
TOP_K = 5
MAX_CONTEXT_LENGTH = 2000

# Flask Configuration
DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
HOST = os.getenv("FLASK_HOST", "0.0.0.0")
PORT = int(os.getenv("FLASK_PORT", "5000"))

# Cache Configuration
CACHE_DIR = os.path.join("D:", "huggingface_cache")
TEMP_DIR = os.path.join("D:", "temp")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = "rag_system.log"

# CORS Configuration
CORS_ORIGINS = ["*"]  # In production, specify exact origins

# Rate Limiting (optional)
RATE_LIMIT_ENABLED = False
MAX_REQUESTS_PER_MINUTE = 10
