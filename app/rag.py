import os
import glob
import numpy as np
from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL, DATA_DIR, TOP_K

# Global storage
chunks = []
embeddings = None
model = None


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



def initialize_rag():
    """Load model, chunk documents, create embeddings"""
    global chunks, embeddings, model
    
    print("🔄 Loading embedding model...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    
    print("🔄 Loading documents...")
    docs = load_documents()
    
    print("🔄 Chunking documents...")
    for doc in docs:
        doc_chunks = chunk_text(doc["content"])
        for chunk in doc_chunks:
            chunks.append({
                "text": chunk,
                "source": doc["filename"]
            })
    
    print(f"✅ Created {len(chunks)} chunks")
    
    print("🔄 Creating embeddings...")
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
    
    print(f"✅ RAG initialized with {len(chunks)} chunks")


def retrieve(query: str, top_k: int = None):
    """Retrieve top-k most relevant chunks for a query"""
    if top_k is None:
        top_k = TOP_K
    
    # Embed query
    query_emb = model.encode([query], convert_to_numpy=True)[0]
    
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