# GitHub Upload Instructions / गिटहब अपलोड निर्देश

## Quick Steps (English)

1. **Initialize Git Repository** (if not already done):
   ```bash
   git init
   ```

2. **Add all files** (large files will be automatically ignored):
   ```bash
   git add .
   ```

3. **Check what will be uploaded**:
   ```bash
   git status
   ```

4. **Commit your changes**:
   ```bash
   git commit -m "Initial commit - RAG Project"
   ```

5. **Create a new repository on GitHub**:
   - Go to https://github.com/new
   - Create a new repository (e.g., "nepali-rag-project")
   - Don't initialize with README

6. **Connect to GitHub and push**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

## हिंदी में निर्देश

1. **Git Repository शुरू करें** (अगर पहले से नहीं है):
   ```bash
   git init
   ```

2. **सभी फाइल्स add करें** (बड़ी files automatically ignore हो जाएंगी):
   ```bash
   git add .
   ```

3. **देखें क्या upload होगा**:
   ```bash
   git status
   ```

4. **Changes को commit करें**:
   ```bash
   git commit -m "Initial commit - RAG Project"
   ```

5. **GitHub पर नया repository बनाएं**:
   - https://github.com/new पर जाएं
   - नया repository बनाएं
   - README के साथ initialize मत करें

6. **GitHub से connect करके push करें**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

## What's Being Uploaded? / क्या अपलोड होगा?

✅ **Will be uploaded:**
- Python code files (app.py, config.py, etc.)
- requirements.txt
- templates/
- README.md and documentation
- Batch files for running server

❌ **Will NOT be uploaded (too large):**
- All corpus directories (ArthaBanijya, Bichar, etc.)
- Vector store directories
- Virtual environment (venv/)
- Large .txt data files
- Model checkpoints
- Jupyter notebooks

## Important Notes

1. **After cloning on new machine**: You'll need to:
   - Run `pip install -r requirements.txt`
   - Add your corpus data back
   - Regenerate vector stores

2. **File size**: GitHub has 100MB file limit. Current .gitignore handles this.

3. **Private vs Public**: Choose private repo if data is sensitive

## Troubleshooting

If you get "file too large" error:
```bash
# Remove file from git tracking
git rm --cached filename.txt
git commit -m "Remove large file"
git push
```

If push is taking too long:
```bash
# Check what's being pushed
git ls-files --others --exclude-standard
```
