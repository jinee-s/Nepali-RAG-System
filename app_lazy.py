"""
Nepali RAG System - Flask API (Lazy Loading Version)
Models are loaded only when first query is made
"""

import os
import pickle
import faiss
import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
FAISS_DIR = r"D:\Nepali_RAG_Project\nepali_vectorstore_bgem3"
MODEL_NAME = "BAAI/bge-m3"
GOOGLE_API_KEY = "AIzaSyD9XJmCg27zvomtrKqz79W1KuyI4HK450Y"
TOP_K = 5

# Global variables - loaded lazily
embedder = None
index = None
texts = None
gemini = None
models_loaded = False


def load_models_lazy():
    """Load models on first request"""
    global embedder, index, texts, gemini, models_loaded
    
    if models_loaded:
        return True
    
    try:
        logger.info("🔄 Loading models (first request)...")
        
        # Load FAISS first (fastest)
        logger.info("📚 Loading FAISS index...")
        index = faiss.read_index(f"{FAISS_DIR}/index.faiss")
        logger.info(f"✓ FAISS: {index.ntotal} vectors")
        
        # Load text metadata
        logger.info("📝 Loading texts...")
        with open(f"{FAISS_DIR}/texts_only.pkl", "rb") as f:
            texts = pickle.load(f)
        logger.info(f"✓ Texts: {len(texts)} entries")
        
        # Load embedding model
        logger.info("🤖 Loading BGE-M3 (this may take a minute)...")
        from sentence_transformers import SentenceTransformer
        embedder = SentenceTransformer(
            MODEL_NAME,
            device='cpu',
            cache_folder=r"D:\huggingface_cache"
        )
        logger.info("✓ BGE-M3 loaded")
        
        # Configure Gemini
        logger.info("🌟 Configuring Gemini...")
        import google.generativeai as genai
        genai.configure(api_key=GOOGLE_API_KEY)
        # Try gemini-2.5-flash which may have different quota
        gemini = genai.GenerativeModel("gemini-2.5-flash")
        logger.info("✓ Gemini configured")
        
        models_loaded = True
        logger.info("✅ All models loaded successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error loading models: {str(e)}")
        return False


def retrieve_context(query, top_k=TOP_K):
    """Retrieve relevant context from FAISS"""
    try:
        q_emb = embedder.encode([query], normalize_embeddings=True)
        scores, ids = index.search(np.array(q_emb, dtype=np.float32), top_k)
        retrieved = [texts[i] for i in ids[0] if 0 <= i < len(texts)]
        return "\n\n".join(retrieved), scores[0].tolist(), ids[0].tolist()
    except Exception as e:
        logger.error(f"Error retrieving: {str(e)}")
        return "", [], []


def generate_answer(question, context):
    """Generate answer using Gemini"""
    prompt = f"""तलका सन्दर्भहरू प्रयोग गरेर तथ्यमा आधारित छोटो उत्तर नेपालीमा लेख।

सन्दर्भहरू:
{context}

प्रश्न: {question}
उत्तर:"""

    try:
        response = gemini.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


@app.route('/')
def home():
    """Main page"""
    return render_template('index.html')


@app.route('/health', methods=['GET'])
def health_check():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': models_loaded,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Main RAG endpoint"""
    try:
        # Load models if not loaded
        if not models_loaded:
            logger.info("⏳ First request - loading models...")
            if not load_models_lazy():
                return jsonify({
                    'success': False,
                    'error': 'Failed to load models'
                }), 500
        
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({'success': False, 'error': 'Question required'}), 400
        
        question = data['question'].strip()
        top_k = data.get('top_k', TOP_K)
        
        logger.info(f"❓ Question: {question}")
        
        # Retrieve and generate
        context, scores, ids = retrieve_context(question, top_k)
        answer = generate_answer(question, context)
        
        return jsonify({
            'success': True,
            'question': question,
            'answer': answer,
            'context': context,
            'scores': scores,
            'retrieved_ids': ids,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/retrieve', methods=['POST'])
def retrieve_only():
    """Retrieve documents only"""
    try:
        if not models_loaded:
            if not load_models_lazy():
                return jsonify({'success': False, 'error': 'Models not loaded'}), 500
        
        data = request.get_json()
        query = data.get('query', '').strip()
        top_k = data.get('top_k', TOP_K)
        
        context, scores, ids = retrieve_context(query, top_k)
        documents = context.split('\n\n') if context else []
        
        return jsonify({
            'success': True,
            'query': query,
            'documents': documents,
            'scores': scores,
            'ids': ids,
            'count': len(documents)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    logger.info("🚀 Starting Nepali RAG System (Lazy Loading Mode)")
    logger.info("📌 Models will load on first request")
    logger.info("🌐 Server starting at http://localhost:5000")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,  # Disable debug for cleaner output
        use_reloader=False  # Disable reloader to avoid double loading
    )
