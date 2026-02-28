%md
# 📦 Installation Guide

## Prerequisites

- **Python 3.8+** - Required for running the chatbot
- **pip** (Python package manager)
- **Databricks account** - For full deployment
- **Google Gemini API key** - [Get one here](https://ai.google.dev/)

---

## Local Installation

### 1. Clone Repository

```bash
git clone https://github.com/Alhaji1015/RAG-CHATBOT-Q-A.git
cd RAG-CHATBOT-Q-A
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Core Dependencies:**
- `google-generativeai>=0.3.0` - Gemini AI API client
- `gradio>=4.0.0` - Web UI framework
- `pandas>=1.5.0` - Data processing
- `ipywidgets>=8.0.0` - Jupyter notebook widgets

### 4. Configure Environment

Create a `.env` file:
```bash
cp config/.env.example config/.env
```

Edit `config/.env` and add your API key:
```
GEMINI_API_KEY=your_api_key_here
MAX_OUTPUT_TOKENS=3500
TEMPERATURE=0.7
```

### 5. Get Gemini API Key

1. Visit: https://ai.google.dev/
2. Sign in with Google account
3. Click **"Get API Key"**
4. Copy your key
5. Add to `config/.env`

---

## Databricks Installation

### Option 1: Using Databricks Repos

1. Go to **Workspace → Repos**
2. Click **"Add Repo"**
3. Enter: `https://github.com/Alhaji1015/RAG-CHATBOT-Q-A`
4. Click **"Create Repo"**

### Option 2: Upload Files

1. Download repository as ZIP
2. Upload to Databricks workspace
3. Extract in your workspace directory

### Configure Databricks Secrets (Recommended)

```python
# In a Databricks notebook
dbutils.secrets.createScope("rag-chatbot")
dbutils.secrets.put("rag-chatbot", "gemini-api-key")
```

Then update your code:
```python
from databricks.sdk.runtime import dbutils
api_key = dbutils.secrets.get(scope="rag-chatbot", key="gemini-api-key")
genai.configure(api_key=api_key)
```

---

## Verify Installation

```python
import google.generativeai as genai
import gradio as gr
import pandas as pd

print("✅ All dependencies installed successfully!")
```

---

## Troubleshooting

### ModuleNotFoundError
```bash
pip install --upgrade google-generativeai gradio pandas
```

### API Key Errors
- Verify key is correct in `config/.env`
- Check for extra spaces or quotes
- Ensure no special characters
- Get a new key if expired

### Databricks Issues
- Use `%pip install` instead of `!pip install`
- Restart Python: `dbutils.library.restartPython()`
- Ensure workspace permissions are correct
- Check cluster has internet access

---

✅ **Installation Complete!** Proceed to Architecture section.
