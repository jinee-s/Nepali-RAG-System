"""
Nepali RAG System - Flask API
Deploys a Question-Answering system using FAISS, BGE-M3, and Google Gemini
"""

import os
import pickle
import faiss
import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for API access

# Configuration
FAISS_DIR = r"D:\Nepali_RAG_Project\nepali_vectorstore_bgem3"
MODEL_NAME = "BAAI/bge-m3"
GOOGLE_API_KEY = "AIzaSyDS1OujZOOCJRLZOxiNqYxOe9Fqu9Ujhc0"  # Move to env var in production
TOP_K = 5

# Global variables for models
embedder = None
index = None
texts = None
gemini = None


def load_models():
    """Load all required models and data"""
    global embedder, index, texts, gemini
    
    try:
        logger.info("Loading BGE-M3 embedding model...")
        # Use the model from cache with explicit cache directory
        import os
        os.environ['HF_HUB_OFFLINE'] = '1'  # Force offline mode
        embedder = SentenceTransformer(
            MODEL_NAME, 
            device='cpu',
            cache_folder=r"D:\huggingface_cache",
            trust_remote_code=False
        )
        logger.info(f"✓ Loaded embedding model: {MODEL_NAME}")
        
        logger.info("Loading FAISS index...")
        index = faiss.read_index(f"{FAISS_DIR}/index.faiss")
        logger.info(f"✓ Loaded FAISS index with {index.ntotal} vectors")
        
        logger.info("Loading text metadata...")
        with open(f"{FAISS_DIR}/texts_only.pkl", "rb") as f:
            texts = pickle.load(f)
        logger.info(f"✓ Loaded {len(texts)} text entries")
        
        logger.info("Configuring Gemini API...")
        genai.configure(api_key=GOOGLE_API_KEY)
        gemini = genai.GenerativeModel("gemini-2.0-flash-exp")
        logger.info("✓ Gemini API configured")
        
        return True
    except Exception as e:
        logger.error(f"✗ Error loading models: {str(e)}")
        return False


def retrieve_context(query, top_k=TOP_K):
    """Retrieve relevant context from FAISS index"""
    try:
        q_emb = embedder.encode([query], normalize_embeddings=True)
        scores, ids = index.search(np.array(q_emb, dtype=np.float32), top_k)
        retrieved = [texts[i] for i in ids[0] if 0 <= i < len(texts)]
        return "\n\n".join(retrieved), scores[0].tolist(), ids[0].tolist()
    except Exception as e:
        logger.error(f"Error retrieving context: {str(e)}")
        return "", [], []


def generate_answer(question, context):
    """Generate answer using Gemini with retrieved context"""
    prompt = f"""तलका सन्दर्भहरू प्रयोग गरेर तथ्यमा आधारित छोटो उत्तर नेपालीमा लेख।
यदि सन्दर्भमा जानकारी छैन भने 'सन्दर्भमा जानकारी उपलब्ध छैन।' भन्नुहोस्।

सन्दर्भहरू:
{context}

प्रश्न: {question}
उत्तर:"""

    try:
        response = gemini.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error generating answer: {str(e)}")
        return f"⚠️ Error: {str(e)}"


@app.route('/')
def home():
    """Render the main web interface"""
    return render_template('index.html')


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': all([embedder, index, texts, gemini]),
        'index_vectors': index.ntotal if index else 0,
        'text_entries': len(texts) if texts else 0
    }
    return jsonify(status)


@app.route('/api/ask', methods=['POST'])
def ask_question():
    """
    Main RAG endpoint - accepts a question and returns an answer
    
    Request body:
    {
        "question": "नेपालको राजधानी के हो?",
        "top_k": 5  (optional, default=5)
    }
    
    Response:
    {
        "question": "...",
        "answer": "...",
        "context": "...",
        "scores": [...],
        "success": true,
        "timestamp": "..."
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({
                'success': False,
                'error': 'Question is required'
            }), 400
        
        question = data['question'].strip()
        top_k = data.get('top_k', TOP_K)
        
        if not question:
            return jsonify({
                'success': False,
                'error': 'Question cannot be empty'
            }), 400
        
        logger.info(f"Processing question: {question}")
        
        # Retrieve context
        context, scores, ids = retrieve_context(question, top_k)
        
        if not context:
            return jsonify({
                'success': False,
                'error': 'Failed to retrieve context'
            }), 500
        
        # Generate answer
        answer = generate_answer(question, context)
        
        response = {
            'success': True,
            'question': question,
            'answer': answer,
            'context': context,
            'scores': scores,
            'retrieved_ids': ids,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Successfully answered question")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/retrieve', methods=['POST'])
def retrieve_only():
    """
    Retrieve relevant documents without generating an answer
    
    Request body:
    {
        "query": "नेपालको राजधानी",
        "top_k": 5  (optional)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'success': False,
                'error': 'Query is required'
            }), 400
        
        query = data['query'].strip()
        top_k = data.get('top_k', TOP_K)
        
        context, scores, ids = retrieve_context(query, top_k)
        
        # Split context back into individual documents
        documents = context.split('\n\n') if context else []
        
        return jsonify({
            'success': True,
            'query': query,
            'documents': documents,
            'scores': scores,
            'ids': ids,
            'count': len(documents),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in retrieve: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


if __name__ == '__main__':
    logger.info("Starting Nepali RAG System...")
    
    # Load models before starting server
    if load_models():
        logger.info("All models loaded successfully!")
        logger.info("Starting Flask server...")
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True
        )
    else:
        logger.error("Failed to load models. Server not started.")
