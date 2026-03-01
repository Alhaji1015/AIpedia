# 🤖 RAG Chatbot — Document Q&A System

[![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=flat&logo=databricks&logoColor=white)](https://databricks.com)
[![Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?style=flat&logo=google&logoColor=white)](https://ai.google.dev/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/Gradio-FF7C00?style=flat&logo=gradio&logoColor=white)](https://gradio.app/)

A production-ready Retrieval-Augmented Generation (RAG) chatbot built with Google Gemini AI and deployed on Databricks Apps. The system enables intelligent Q&A over your document corpus with source attribution and semantic search.

**🌐 Live Demo:** [rag-chatbot-7474659359669446.aws.databricksapps.com](https://rag-chatbot-7474659359669446.aws.databricksapps.com/)
[Watch demo video](https://youtu.be/w1zpi4Z4n6c)
---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## Features

| Feature | Description |
|---|---|
| 🔍 Intelligent Retrieval | Keyword-based search with smart ranking |
| 🤖 AI-Powered Responses | Powered by Google Gemini 2.5 Flash |
| 📚 Multi-Document Support | Query across multiple documents simultaneously |
| 🎯 Source Attribution | Every answer cites its source documents |
| ⚡ Smart Context Detection | Automatically adjusts retrieval for summary vs. specific queries |
| 💬 Conversational Memory | Maintains context across conversation turns |
| 🎨 User-Friendly Interface | Gradio-based chat UI with example questions |
| 🚀 Production-Ready | Deployed as a Databricks App with scalability |
| 📊 Configurable Parameters | Adjustable token limits, temperature, and retrieval settings |

---

## Architecture

```
┌─────────────────────────────────────┐
│      USER INTERFACE (Gradio)        │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│    RAG CHATBOT AGENT                │
│  1. Query Processing                │
│  2. Smart Retrieval                 │
│  3. Document Retrieval              │
│  4. Context Building                │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│    DOCUMENT REPOSITORY              │
│    (7 PDFs, ~616 KB)                │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│    GOOGLE GEMINI 2.5 FLASH          │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│    RESPONSE GENERATION              │
└─────────────────────────────────────┘
```

---

## Quick Start

```bash
# Clone and install
git clone https://github.com/Alhaji1015/RAG-CHATBOT-Q-A.git
cd RAG-CHATBOT-Q-A
pip install -r requirements.txt

# Set up environment
cp config/.env.example config/.env
# Add your Gemini API key to config/.env

# Run locally
python src/app.py
```

Then visit `http://localhost:8000` to use the chatbot.

---

## Documentation

| Guide | Description |
|---|---|
| [Installation](docs/INSTALLATION.md) | Detailed setup instructions |
| [Architecture](docs/ARCHITECTURE.md) | System design and components |
| [API Reference](docs/API.md) | Code documentation |
| [Deployment](docs/DEPLOYMENT.md) | Production deployment guide |

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Author

**Darlington Omoruyi**

- GitHub: [@Alhaji1015](https://github.com/Alhaji1015)
- Project: [RAG-CHATBOT-Q-A](https://github.com/Alhaji1015/RAG-CHATBOT-Q-A)
- Live Demo: [RAG Chatbot](https://rag-chatbot-7474659359669446.aws.databricksapps.com/)

---

## Acknowledgments

- [Google Gemini](https://ai.google.dev/) — AI capabilities
- [Databricks](https://databricks.com) — Deployment platform
- [Gradio](https://gradio.app/) — UI framework
