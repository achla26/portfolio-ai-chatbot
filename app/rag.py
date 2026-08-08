import os
import glob
import cohere
import numpy as np
from app.config import DATA_DIR, TOP_K, COHERE_API_KEY

# Global storage
chunks = []
embeddings = None
cohere_client = None


def load_documents():
    """Load all .md files from data folder"""
    docs = []
    files = glob.glob(os.path.join(DATA_DIR, "*.md"))
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            filename = os.path.basename(file)
            docs.append({"filename": filename, "content": content})
    return docs


def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50):
    """Split text into overlapping chunks"""
    words = text.split()
    result = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        result.append(chunk)
        i += chunk_size - overlap
    return result


def embed_texts(texts: list, input_type: str = "search_document") -> np.ndarray:
    """Embed texts using Cohere API"""
    global cohere_client
    
    response = cohere_client.embed(
        texts=texts,
        model="embed-english-light-v3.0",
        input_type=input_type,
    )
    
    return np.array(response.embeddings)


def initialize_rag():
    """Load documents and create embeddings via Cohere"""
    global chunks, embeddings, cohere_client
    
    print("🔄 Initializing Cohere client...")
    if not COHERE_API_KEY:
        raise ValueError("❌ COHERE_API_KEY not set in environment!")
    
    cohere_client = cohere.Client(COHERE_API_KEY)
    print("✅ Cohere client ready")
    
    print("🔄 Loading documents...")
    docs = load_documents()
    print(f"✅ Loaded {len(docs)} documents")
    
    print("🔄 Chunking documents...")
    for doc in docs:
        doc_chunks = chunk_text(doc["content"])
        for chunk in doc_chunks:
            chunks.append({
                "text": chunk,
                "source": doc["filename"]
            })
    
    print(f"✅ Created {len(chunks)} chunks")
    
    print("🔄 Creating embeddings via Cohere API...")
    texts = [c["text"] for c in chunks]
    embeddings = embed_texts(texts, input_type="search_document")
    
    print(f"✅ RAG initialized with {len(chunks)} chunks")
    print(f"✅ Embeddings shape: {embeddings.shape}")


def retrieve(query: str, top_k: int = None):
    """Retrieve top-k most relevant chunks for a query"""
    if top_k is None:
        top_k = TOP_K
    
    # Embed query using "search_query" type
    query_emb = embed_texts([query], input_type="search_query")[0]
    
    # Cosine similarity
    similarities = np.dot(embeddings, query_emb) / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_emb) + 1e-8
    )
    
    # Get top-k indices
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    
    results = []
    for idx in top_indices:
        results.append({
            "text": chunks[idx]["text"],
            "source": chunks[idx]["source"],
            "score": float(similarities[idx])
        })
    
    return results


def get_context(query: str, top_k: int = None):
    """Get formatted context string from retrieved chunks"""
    results = retrieve(query, top_k)
    context = "\n\n---\n\n".join([r["text"] for r in results])
    return context, results