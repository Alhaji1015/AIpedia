%md
# 🏗️ Architecture Guide

## System Overview

The RAG Chatbot uses **Retrieval-Augmented Generation (RAG)** architecture to answer questions based on document content with source attribution.

---

## System Design Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                         │
│              (Gradio Web UI / ipywidgets)                       │
│  • Text input for questions                                     │
│  • Streaming responses with markdown                            │
│  • Example questions & conversation history                     │
│  • Source citations display                                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RAG CHATBOT AGENT                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  1. Query Processing                                     │  │
│  │     • Tokenize user question                             │  │
│  │     • Detect intent (summary vs specific)                │  │
│  │     • Extract keywords                                   │  │
│  │                                                           │  │
│  │  2. Smart Retrieval Selection                            │  │
│  │     • Summary keywords? → ALL 7 documents                │  │
│  │     • Specific query? → TOP 3 documents                  │  │
│  │     • Custom top_k parameter support                     │  │
│  │                                                           │  │
│  │  3. Document Retrieval                                   │  │
│  │     • Keyword matching algorithm                         │  │
│  │     • TF-based scoring                                   │  │
│  │     • Rank by relevance score                            │  │
│  │                                                           │  │
│  │  4. Context Building                                     │  │
│  │     • Extract 4000 chars per document                    │  │
│  │     • Format as structured prompt                        │  │
│  │     • Include document metadata (filename, path)         │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  DOCUMENT REPOSITORY                            │
│                                                                 │
│  📄 Table: workspace.default.ai_documents_parsed                │
│                                                                 │
│  Documents (7 total, ~616 KB):                                 │
│  ├─ 22365_3_Prompt Engineering_v7.pdf                          │
│  ├─ Foundational Large Language Models & Text Generation       │
│  ├─ Embeddings & Vector Stores                                 │
│  ├─ Solving Domain-Specific Problems Using LLMs                │
│  ├─ Evaluating LLMs                                            │
│  ├─ GenAI Agents                                               │
│  └─ Operationalizing GenAI on Vertex AI using MLOps            │
│                                                                 │
│  Fields: filename, full_text, path                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              GOOGLE GEMINI 2.5 FLASH API                        │
│                                                                 │
│  Configuration:                                                 │
│  ├─ Model: gemini-2.5-flash                                    │
│  ├─ Max Output Tokens: 3500                                    │
│  ├─ Temperature: 0.7 (balanced creativity)                     │
│  ├─ Context Window: 4000 chars per doc × K docs                │
│  ├─ Conversation Memory: Maintained across turns               │
│  └─ Streaming: Supported                                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RESPONSE GENERATION                          │
│                                                                 │
│  Output Components:                                             │
│  ├─ AI-generated answer (context-aware)                        │
│  ├─ Source citations (document filenames)                      │
│  ├─ Formatted with markdown                                    │
│  ├─ Conversation history tracking                              │
│  └─ Error handling & fallbacks                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

```
📝 User Question
    │
    ├─► Keyword Extraction (regex tokenization)
    │
    ├─► Intent Detection
    │   ├─ Summary keywords? → top_k = 7
    │   └─ Specific query? → top_k = 3
    │
    ├─► Document Retrieval
    │   ├─► Keyword matching across documents
    │   ├─► Relevance scoring (match count)
    │   └─► Top-K selection
    │
    ├─► Context Assembly
    │   ├─ 4000 chars × K documents
    │   ├─ Document metadata inclusion
    │   └─ Structured prompt formatting
    │
    ├─► Prompt Construction
    │   ├─► System prompt (first message)
    │   ├─► Document context
    │   ├─► User question
    │   └─► Conversation history
    │
    ├─► Gemini API Call
    │   ├─► Generate response (max 3500 tokens)
    │   ├─► Temperature: 0.7
    │   └─► Maintain conversation state
    │
    └─► Response Display
        ├─► Answer text
        ├─► Source citations
        └─► Conversation history update
```

---

## Key Components

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Gradio + ipywidgets | Chat interface, widgets |
| **Backend** | Python 3.8+ | RAG logic, orchestration |
| **LLM** | Google Gemini 2.5 Flash | Response generation |
| **Document Store** | Databricks Table | 7 PDFs (parsed text) |
| **Retrieval** | Keyword Matching | TF-based scoring |
| **Deployment** | Databricks Apps | Production hosting |
| **Notebook** | Databricks | Development environment |

---

## Smart Context Detection

The system automatically detects query intent:

**Summary Queries** (uses ALL 7 documents):
- Keywords: "all", "summary", "summarize", "overview"
- Keywords: "what topics", "covered", "documents"
- Example: "Provide a summary of all documents"

**Specific Queries** (uses TOP 3 documents):
- Default behavior for focused questions
- Example: "What is prompt engineering?"

**Manual Override**:
```python
response, sources = rag_chatbot.ask("question", top_k=5)
```

---

## Scalability & Performance

- **Documents**: Can handle 100+ documents
- **Queries**: Stateless per request (no shared state)
- **Concurrent Users**: Supported by Databricks Apps
- **Response Time**: ~2-5 seconds per query
- **Context Size**: 4000 chars × K docs (max ~28KB for 7 docs)
- **Token Limit**: 3500 output tokens (~2500 words)

---

## Future Enhancements

- 🔄 Semantic search with embeddings (vs keyword matching)
- 📊 Vector database integration (Chroma, Pinecone)
- 🌐 Multi-language support
- 🔄 Real-time document updates via API
- 👥 User authentication & access control
- 📈 Analytics dashboard
- 🔍 Advanced filtering options
