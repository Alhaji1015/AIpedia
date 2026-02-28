%md
# 📚 API Reference

## RAGChatbotAgent Class

### Constructor

```python
RAGChatbotAgent(documents, system_prompt)
```

**Parameters:**
- `documents` (list): List of document dictionaries with keys:
  - `filename` (str): Document filename
  - `full_text` (str): Full document text content
  - `path` (str): Document storage path
- `system_prompt` (str): System instructions for the AI agent

**Returns:** `RAGChatbotAgent` instance

**Example:**
```python
agent = RAGChatbotAgent(
    documents=documents,
    system_prompt="You are a helpful assistant."
)
```

---

### Methods

#### `ask(question, top_k=None)`

Ask a question and get AI-generated response with source attribution.

**Parameters:**
- `question` (str): User question
- `top_k` (int, optional): Number of documents to retrieve
  - `None` (default): Auto-detect (3 for specific, 7 for summaries)
  - `1-N`: Custom number of documents

**Returns:**
- `tuple`: `(response_text, sources)`
  - `response_text` (str): AI-generated answer
  - `sources` (list): Retrieved documents with metadata

**Example:**
```python
# Auto-detect retrieval count
response, sources = agent.ask("What is prompt engineering?")
print(response)

# Use all documents
response, sources = agent.ask("Summarize all documents", top_k=7)

# Use specific number
response, sources = agent.ask("Question", top_k=5)
```

#### `show_history()`

Display complete conversation history with sources.

**Parameters:** None

**Returns:** None (prints to console)

**Example:**
```python
agent.show_history()
```

**Output:**
```
[Turn 1]
User: What is prompt engineering?
Agent: Prompt engineering is...
Sources: doc1.pdf, doc2.pdf
```

---

### Attributes

- `model` (GenerativeModel): Gemini model instance
- `documents` (list): List of source documents
- `system_prompt` (str): System instructions
- `chat` (ChatSession): Active chat session
- `conversation_history` (list): List of conversation turns
- `generation_config` (GenerationConfig): LLM generation parameters

---

## retrieve_relevant_documents Function

```python
retrieve_relevant_documents(query, documents, top_k=3)
```

**Parameters:**
- `query` (str): Search query
- `documents` (list): Document corpus
- `top_k` (int): Number of documents to return (default: 3)

**Returns:**
- `list`: Scored documents with previews

**Return Structure:**
```python
[
    {
        'doc': {'filename': 'doc.pdf', 'full_text': '...', 'path': '...'},
        'score': 5,  # Number of keyword matches
        'preview': 'First 4000 chars...'  # Document preview
    },
    ...
]
```

**Example:**
```python
results = retrieve_relevant_documents(
    "prompt engineering",
    documents,
    top_k=5
)

for item in results:
    print(f"{item['doc']['filename']}: Score {item['score']}")
```

---

## Configuration Objects

### GenerationConfig

```python
genai.GenerationConfig(
    max_output_tokens=3500,
    temperature=0.7,
)
```

**Parameters:**

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `max_output_tokens` | int | 1-8192 | 3500 | Maximum response length |
| `temperature` | float | 0.0-1.0 | 0.7 | Creativity level |
| `top_k` | int | 1-40 | - | Token selection diversity |
| `top_p` | float | 0.0-1.0 | - | Nucleus sampling |

**Temperature Guide:**
- `0.0`: Deterministic, conservative
- `0.3-0.5`: Balanced, focused
- `0.7`: Creative, diverse (recommended)
- `1.0`: Highly creative, random

---

## Environment Variables

```python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
max_tokens = int(os.getenv('MAX_OUTPUT_TOKENS', 3500))
temperature = float(os.getenv('TEMPERATURE', 0.7))
```

**Required:**
- `GEMINI_API_KEY` - Your Gemini API key

**Optional:**
- `MAX_OUTPUT_TOKENS` (default: 3500)
- `TEMPERATURE` (default: 0.7)
- `DEFAULT_TOP_K` (default: 3)

---

## Error Handling

```python
try:
    response, sources = agent.ask("question")
except Exception as e:
    print(f"Error: {e}")
```

**Common Errors:**
- `InvalidArgument`: API key expired/invalid
- `PermissionDenied`: API key reported as leaked
- `ResourceExhausted`: Rate limit exceeded
- `ModuleNotFoundError`: Missing dependencies

---

## Usage Examples

### Basic Usage

```python
# Initialize
agent = RAGChatbotAgent(documents, "You are helpful.")

# Ask question
response, sources = agent.ask("What is AI?")
print(response)
```

### With Custom Parameters

```python
# Use all documents
response, sources = agent.ask(
    "Provide comprehensive summary",
    top_k=len(documents)
)
```

### Check Sources

```python
response, sources = agent.ask("question")

for source in sources:
    print(f"Document: {source['doc']['filename']}")
    print(f"Score: {source['score']}")
    print(f"Preview: {source['preview'][:100]}...")
```

### Conversation Flow

```python
# Question 1
response1, _ = agent.ask("What is prompt engineering?")

# Follow-up (maintains context)
response2, _ = agent.ask("Can you give examples?")

# View history
agent.show_history()
```
