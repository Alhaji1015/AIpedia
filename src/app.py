
!pip install gradioimport gradio as gr

import google.generativeai as genai
import pandas as pd
from pyspark.sql import SparkSession

# Initialize Spark
spark = SparkSession.builder.getOrCreate()

# Configure Gemini API
genai.configure(api_key='Your_API_KEY')

# Load documents from table
def load_documents():
    try:
        documents_df = spark.sql("""
            SELECT filename, full_text, path
            FROM workspace.default.ai_documents_parsed
            WHERE full_text IS NOT NULL
            LIMIT 100
        """)
        documents = documents_df.toPandas().to_dict('records')
        return documents
    except Exception as e:
        print(f"Error loading documents: {e}")
        return []

# Retrieval function
def retrieve_relevant_documents(query, documents, top_k=3):
    import re
    query_words = set(re.findall(r'\w+', query.lower()))
    scored_docs = []
    for doc in documents:
        text = doc.get('full_text', '').lower()
        matches = sum(1 for word in query_words if word in text)
        if matches > 0:
            scored_docs.append({
                'doc': doc,
                'score': matches,
                'preview': doc['full_text'][:4000] if doc['full_text'] else ''
            })
    scored_docs.sort(key=lambda x: x['score'], reverse=True)
    return scored_docs[:top_k]

# RAG Chatbot Agent
class RAGChatbotAgent:
    def __init__(self, documents, system_prompt):
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.documents = documents
        self.system_prompt = system_prompt
        self.chat = self.model.start_chat(history=[])
        self.conversation_history = []
        self.generation_config = genai.GenerationConfig(
            max_output_tokens=3500,
            temperature=0.7,
        )
    
    def ask(self, question, top_k=None):
        if top_k is None:
            summary_keywords = ['all', 'summary', 'summarize', 'overview', 'what topics', 'covered', 'documents']
            if any(keyword in question.lower() for keyword in summary_keywords):
                top_k = len(self.documents)
            else:
                top_k = 3
        
        relevant_docs = retrieve_relevant_documents(question, self.documents, top_k=top_k)
        
        context = ""
        if relevant_docs:
            context = "\n\nRelevant documents:\n"
            for i, item in enumerate(relevant_docs, 1):
                doc = item['doc']
                preview = item['preview']
                context += f"\n[Document {i}: {doc['filename']}]\n{preview}\n"
        
        if len(self.conversation_history) == 0:
            full_prompt = f"{self.system_prompt}{context}\n\nUser: {question}"
        else:
            full_prompt = f"{question}{context}"
        
        response = self.chat.send_message(full_prompt, generation_config=self.generation_config)
        
        self.conversation_history.append({
            "user": question,
            "agent": response.text,
            "retrieved_docs": [item['doc']['filename'] for item in relevant_docs]
        })
        
        return response.text, relevant_docs

# Initialize chatbot
print("🚀 Loading documents...")
documents = load_documents()
print(f"✅ Loaded {len(documents)} documents")

rag_chatbot = RAGChatbotAgent(
    documents=documents,
    system_prompt="You are a helpful AI assistant. Answer questions based on the provided documents. If the information is not in the documents, say so."
)

# Gradio interface
def chat_interface(message, history):
    if not message.strip():
        return ""
    
    try:
        response, sources = rag_chatbot.ask(message)
        if sources:
            source_names = [s['doc']['filename'] for s in sources]
            response += f"\n\n📚 **Sources:** {', '.join(source_names)}"
        return response
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Create Gradio app
demo = gr.ChatInterface(
    fn=chat_interface,
    title="🤖 RAG Chatbot - Document Q&A",
    description=f"Ask questions about {len(documents)} documents on LLMs, Prompt Engineering, and Generative AI.",
    examples=[
        "What is prompt engineering?",
        "How do I evaluate LLMs?",
        "Provide a summary of all documents",
        "What are best practices for prompt engineering?",
        "Explain embeddings and vector stores"
    ]
)

if __name__ == "__main__":
    demo.launch()
