%md
# 🚀 Deployment Guide

## Databricks Apps Deployment

### Prerequisites

- ✅ Databricks workspace (AWS/Azure/GCP)
- ✅ Databricks CLI installed
- ✅ Personal access token
- ✅ Updated app.py with correct API key

---

### Step 1: Prepare Files

Ensure your deployment directory contains:

```
/Workspace/Users/your-email@databricks.com/rag_chatbot_app/
├── app.py                 # Main application
├── documents.json         # Pre-loaded documents (616 KB)
├── app.yaml              # Databricks configuration
└── requirements.txt      # Python dependencies
```

---

### Step 2: Update app.py

**Option A: Use Environment Variables (Recommended)**

```python
import os
import google.generativeai as genai

# Load from environment
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)
```

**Option B: Use Databricks Secrets (Production)**

```python
from databricks.sdk.runtime import dbutils

api_key = dbutils.secrets.get(
    scope="rag-chatbot",
    key="gemini-api-key"
)
genai.configure(api_key=api_key)
```

---

### Step 3: Create Databricks Secrets

```bash
# Create secret scope
databricks secrets create-scope rag-chatbot

# Add API key
databricks secrets put-secret rag-chatbot gemini-api-key
# (You'll be prompted to enter your key)
```

**Verify:**
```bash
databricks secrets list-scopes
databricks secrets list rag-chatbot
```

---

### Step 4: Deploy the App

#### Option A: Databricks CLI (Recommended)

```bash
# Navigate to your app directory
cd /local/path/to/rag-chatbot

# Upload to Databricks workspace
databricks workspace import-dir . \
  /Workspace/Users/your-email@databricks.com/rag_chatbot_app

# Deploy app
databricks apps deploy rag-chatbot \
  --source-code-path /Workspace/Users/your-email@databricks.com/rag_chatbot_app
```

#### Option B: Databricks UI

1. Go to **Workspace → Apps**
2. Click **"Create App"**
3. Fill in:
   - **App name:** `rag-chatbot`
   - **Source path:** `/Workspace/Users/your-email@databricks.com/rag_chatbot_app`
   - **Compute:** Serverless (recommended)
4. Click **"Deploy"**
5. Wait 2-5 minutes for deployment

---

### Step 5: Access Your App

Your app will be available at:
```
https://your-workspace.cloud.databricks.com/apps/rag-chatbot
```

**Check Status:**
- Green: Running ✅
- Yellow: Starting ⏳
- Red: Error ❌

---

## Local Deployment

### Run Locally for Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment
export GEMINI_API_KEY=your_key_here

# Run app
python app.py
```

Access at: `http://localhost:8000`

---

## Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .
COPY documents.json .

# Environment
ENV GEMINI_API_KEY=""
ENV PORT=8000

EXPOSE 8000

CMD ["python", "app.py"]
```

### Build and Run

```bash
# Build image
docker build -t rag-chatbot:latest .

# Run container
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  rag-chatbot:latest
```

---

## Cloud Deployment Options

### AWS EC2

```bash
# Launch instance (t2.medium recommended)
aws ec2 run-instances \
  --image-id ami-xxx \
  --instance-type t2.medium

# SSH and install
ssh ec2-user@instance-ip
sudo yum install python3 git
git clone https://github.com/Alhaji1015/RAG-CHATBOT-Q-A.git
cd RAG-CHATBOT-Q-A
pip3 install -r requirements.txt
python3 app.py
```

### Azure Container Instances

```bash
az container create \
  --resource-group myResourceGroup \
  --name rag-chatbot \
  --image rag-chatbot:latest \
  --ports 8000 \
  --environment-variables GEMINI_API_KEY=your_key
```

### GCP Cloud Run

```bash
gcloud run deploy rag-chatbot \
  --image rag-chatbot:latest \
  --platform managed \
  --port 8000 \
  --set-env-vars GEMINI_API_KEY=your_key
```

---

## Monitoring & Troubleshooting

### Check Logs

**Databricks Apps:**
```python
# In notebook
dbutils.apps.getLogs("rag-chatbot")
```

**CLI:**
```bash
databricks apps logs rag-chatbot
```

### Common Issues

| Issue | Solution |
|-------|----------|
| App won't start | Check logs, verify API key, ensure all files present |
| Slow performance | Increase compute, reduce document size, lower max_tokens |
| Connection timeout | Check firewall, verify ports open (8000) |
| Import errors | Verify requirements.txt, check Python version |
| API key errors | Use Databricks secrets, verify key is valid |

### Health Check

```bash
curl https://your-app-url/
# Should return 200 OK
```

---

## Security Best Practices

1. ✅ **Use Secrets Management**
   - Never hardcode API keys
   - Use Databricks secrets or env vars

2. ✅ **Enable HTTPS**
   - Databricks Apps: Automatic
   - Self-hosted: Use Let's Encrypt

3. ✅ **Restrict Network Access**
   - Configure firewall rules
   - Use VPC/private endpoints

4. ✅ **Monitor Access Logs**
   - Track usage patterns
   - Alert on anomalies

5. ✅ **Regular Updates**
   - Keep dependencies current
   - Update API keys periodically

6. ✅ **Rate Limiting**
   - Implement request throttling
   - Protect against abuse

---

## Scaling Strategies

### Horizontal Scaling
- Deploy multiple app instances
- Use load balancer (AWS ALB, Azure Load Balancer)
- Share document store across instances

### Vertical Scaling
- Increase compute resources
- Optimize memory usage
- Cache responses

### Performance Optimization
- Use vector database for semantic search
- Implement response caching
- Batch document processing
- Async request handling

---

## CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy to Databricks

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Databricks
        run: |
          databricks apps deploy rag-chatbot \
            --source-code-path .
        env:
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
```

---

## Production Checklist

- [ ] API keys in secrets (not hardcoded)
- [ ] HTTPS enabled
- [ ] Monitoring configured
- [ ] Error logging set up
- [ ] Rate limiting implemented
- [ ] Health checks configured
- [ ] Backup strategy defined
- [ ] Documentation updated
- [ ] Testing completed
- [ ] Security audit passed

---

✅ **Your RAG Chatbot is Production-Ready!**

**Live App:** https://rag-chatbot-7474659359669446.aws.databricksapps.com/
