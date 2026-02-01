# Nepali RAG System - Flask Deployment 🇳🇵

A production-ready Flask web application for deploying a Retrieval-Augmented Generation (RAG) system for Nepali language Question-Answering using FAISS, BGE-M3 embeddings, and Google Gemini.

## 🚀 Features

- **Fast Semantic Search**: Uses FAISS vector database with 100K+ Nepali text entries
- **Powerful Embeddings**: BGE-M3 multilingual embeddings optimized for Nepali
- **AI-Powered Answers**: Google Gemini 2.0 Flash for natural language generation
- **RESTful API**: Clean API endpoints for integration
- **Beautiful UI**: Nepali-friendly web interface with Devanagari support
- **Production Ready**: Configured for deployment with Gunicorn

## 📁 Project Structure

```
RAG_PROJECT_NEW/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html             # Web interface
├── nepali_vectorstore_bgem3/  # FAISS index and metadata
│   ├── index.faiss
│   └── texts_only.pkl
└── README.md                   # This file
```

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- At least 4GB RAM
- FAISS index files (already created in your workspace)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Environment Variables (Optional)

Create a `.env` file for sensitive information:

```bash
GOOGLE_API_KEY=your_api_key_here
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

### Step 3: Verify FAISS Index

Make sure the FAISS index exists at:
```
D:\Nepali_RAG_Project\nepali_vectorstore_bgem3\index.faiss
D:\Nepali_RAG_Project\nepali_vectorstore_bgem3\texts_only.pkl
```

## 🎯 Running the Application

### Development Mode

```bash
python app.py
```

The server will start at `http://localhost:5000`

### Production Mode with Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app --timeout 120
```

Options:
- `-w 4`: Use 4 worker processes
- `-b 0.0.0.0:5000`: Bind to all interfaces on port 5000
- `--timeout 120`: Set timeout to 120 seconds

## 📡 API Endpoints

### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-09T10:30:00",
  "models_loaded": true,
  "index_vectors": 100000,
  "text_entries": 100000
}
```

### 2. Ask Question (Main RAG Endpoint)
```http
POST /api/ask
Content-Type: application/json

{
  "question": "नेपालको राजधानी के हो?",
  "top_k": 5
}
```

**Response:**
```json
{
  "success": true,
  "question": "नेपालको राजधानी के हो?",
  "answer": "काठमाडौं",
  "context": "Retrieved context...",
  "scores": [0.89, 0.85, 0.82, 0.78, 0.75],
  "retrieved_ids": [1234, 5678, ...],
  "timestamp": "2025-12-09T10:30:00"
}
```

### 3. Retrieve Documents Only
```http
POST /api/retrieve
Content-Type: application/json

{
  "query": "नेपालको राजधानी",
  "top_k": 5
}
```

**Response:**
```json
{
  "success": true,
  "query": "नेपालको राजधानी",
  "documents": ["doc1", "doc2", ...],
  "scores": [0.89, 0.85, ...],
  "ids": [1234, 5678, ...],
  "count": 5,
  "timestamp": "2025-12-09T10:30:00"
}
```

## 🌐 Web Interface

Access the web interface at `http://localhost:5000`

Features:
- Beautiful Nepali-friendly UI
- Real-time question answering
- Display of retrieved context
- Example questions for quick testing
- Responsive design for mobile devices

## 🧪 Testing with cURL

```bash
# Health check
curl http://localhost:5000/health

# Ask a question
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"नेपालको राजधानी के हो?\"}"

# Retrieve documents
curl -X POST http://localhost:5000/api/retrieve \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"नेपाल\"}"
```

## 🧪 Testing with Python

```python
import requests

# Ask a question
response = requests.post(
    'http://localhost:5000/api/ask',
    json={'question': 'नेपालको राजधानी के हो?'}
)

data = response.json()
print(data['answer'])
```

## 🐳 Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app", "--timeout", "120"]
```

Build and run:
```bash
docker build -t nepali-rag .
docker run -p 5000:5000 -v D:/Nepali_RAG_Project:/data nepali-rag
```

## ⚙️ Configuration

Edit `config.py` to customize:

- `MODEL_NAME`: Embedding model
- `FAISS_DIR`: Path to FAISS index
- `TOP_K`: Number of documents to retrieve
- `GEMINI_MODEL`: Gemini model version
- `HOST` and `PORT`: Server settings

## 🔐 Security Best Practices

1. **API Key Management**: 
   - Never commit API keys to version control
   - Use environment variables or secret management services

2. **CORS Configuration**:
   - In production, specify exact allowed origins in `config.py`

3. **Rate Limiting**:
   - Implement rate limiting for public APIs
   - Use Flask-Limiter or similar extensions

4. **HTTPS**:
   - Use HTTPS in production with SSL certificates
   - Deploy behind a reverse proxy (Nginx, Apache)

## 📊 Performance Optimization

- **Caching**: Implement Redis for caching frequent queries
- **Load Balancing**: Use multiple workers with Gunicorn
- **Async Processing**: Consider Celery for long-running tasks
- **CDN**: Serve static files via CDN

## 🐛 Troubleshooting

### Issue: Models not loading
- **Solution**: Check FAISS_DIR path in config.py
- Verify index files exist and are not corrupted

### Issue: Out of memory
- **Solution**: Reduce batch size or use smaller model
- Use FAISS IndexIVFFlat instead of IndexFlatIP

### Issue: Slow response times
- **Solution**: Increase worker count in Gunicorn
- Optimize TOP_K parameter
- Use faster Gemini model variant

## 📝 Example Questions

- नेपालको राजधानी के हो?
- नेपालमा कति वटा प्रदेश छन्?
- सगरमाथाको उचाइ कति छ?
- नेपालको राष्ट्रिय भाषा के हो?
- गण्डकी प्रदेशको राजधानी कहाँ हो?

## 📄 License

This project is for educational purposes.

## 🤝 Contributing

Contributions are welcome! Please open issues or submit pull requests.

## 📧 Support

For issues or questions, please create a GitHub issue.

---

**Built with ❤️ for Nepali NLP**
