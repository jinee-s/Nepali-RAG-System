# Data Setup Instructions

## Large Files Not Included in Git

Due to GitHub size limitations, the following directories and files are excluded from the repository:

### Corpus Data Directories (Not in Git)
- `ArthaBanijya/` - Economics/Business articles
- `Bichar/` - Opinion articles
- `Desh/` - National news
- `Khelkud/` - Sports articles
- `Manoranjan/` - Entertainment
- `Prabas/` - Travel/Migration
- `Sahitya/` - Literature
- `SuchanaPrabidhi/` - Technology
- `Swasthya/` - Health
- `Viswa/` - International news
- `train/` - Training data
- `valid/` - Validation data

### Vector Store Directories (Not in Git)
- `nepali_vectorstore_bgem3/`
- `nepali_vectorstore_fast/`
- `nepali_vectorstore_full/`
- `nepali_vectorstore_partial/`
- `checkpoints/`

### Large Data Files (Not in Git)
- `cleaned_nepali_corpus.txt`
- `ne_dedup.txt`
- `evaluation_data.csv`
- `evaluation_set.csv`

## How to Set Up Data Locally

1. **Download or prepare your corpus data** - Place text files in respective category directories
2. **Run the data processing script** - Process and create vector stores
3. **Configure paths** - Update paths in `config.py` if needed

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
# or for lazy loading
python app_lazy.py
```

## Note for Deployment

For production deployment (e.g., on Render, Heroku), you'll need to:
1. Upload corpus data separately or use cloud storage (S3, Google Cloud Storage)
2. Generate vector stores on first run or pre-generate and upload them
3. Set appropriate environment variables in `.env` file
