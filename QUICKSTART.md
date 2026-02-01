# Quick Start Guide - Nepali RAG Flask Deployment

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies

Open PowerShell in the project directory and run:

```powershell
pip install -r requirements.txt
```

### Step 2: Start the Server

**Option A: Using the startup script (Recommended)**
```powershell
.\start_server.bat
```

**Option B: Manual start**
```powershell
python app.py
```

### Step 3: Open Your Browser

Visit: `http://localhost:5000`

---

## 📝 What You'll See

1. **Web Interface**: Beautiful Nepali UI to ask questions
2. **API Endpoints**: RESTful API at `/api/ask` and `/api/retrieve`
3. **Health Check**: Monitor system at `/health`

---

## 🧪 Test the API

After starting the server, run the test script:

```powershell
python test_api.py
```

---

## ❓ Example Questions to Try

- नेपालको राजधानी के हो?
- नेपालमा कति वटा प्रदेश छन्?
- सगरमाथाको उचाइ कति छ?
- नेपालको राष्ट्रिय भाषा के हो?
- गण्डकी प्रदेशको राजधानी कहाँ हो?

---

## 🔧 Troubleshooting

### Server won't start?

1. **Check Python version**: Must be 3.8+
   ```powershell
   python --version
   ```

2. **Check FAISS index exists**:
   ```
   D:\Nepali_RAG_Project\nepali_vectorstore_bgem3\index.faiss
   D:\Nepali_RAG_Project\nepali_vectorstore_bgem3\texts_only.pkl
   ```

3. **Check API key**: Update `GOOGLE_API_KEY` in `config.py`

### Slow responses?

- First query loads models (takes 10-30 seconds)
- Subsequent queries are faster (2-5 seconds)

### Out of memory?

- Close other applications
- Reduce `TOP_K` in `config.py`

---

## 📱 Using the API from Other Apps

### Python Example
```python
import requests

response = requests.post(
    'http://localhost:5000/api/ask',
    json={'question': 'नेपालको राजधानी के हो?'}
)

print(response.json()['answer'])
```

### JavaScript Example
```javascript
fetch('http://localhost:5000/api/ask', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({question: 'नेपालको राजधानी के हो?'})
})
.then(r => r.json())
.then(data => console.log(data.answer));
```

### cURL Example
```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "नेपालको राजधानी के हो?"}'
```

---

## 🌐 Deploy to Production

### Option 1: Local Server with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app --timeout 120
```

### Option 2: Cloud Platforms

**Heroku**:
1. Add `Procfile`: `web: gunicorn app:app`
2. Deploy: `git push heroku main`

**AWS EC2**:
1. Upload files to EC2
2. Install dependencies
3. Run with Gunicorn behind Nginx

**Google Cloud Run**:
1. Create Dockerfile
2. Build and deploy: `gcloud run deploy`

---

## 🔒 Security Checklist for Production

- [ ] Move API key to environment variable
- [ ] Enable HTTPS
- [ ] Add rate limiting
- [ ] Restrict CORS origins
- [ ] Add authentication
- [ ] Enable logging
- [ ] Set up monitoring

---

## 📞 Need Help?

Check the full `README.md` for detailed documentation.

---

**Happy Deploying! 🎉**
