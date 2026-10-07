# Portfolio AI Chatbot — RAG Backend

FastAPI backend for the AI chat on [achla-dev.vercel.app](https://achla-dev.vercel.app/chat).
Retrieval over my own career knowledge base (`data/*.md`) + Groq LLM (Llama 3.3) + SSE streaming + rate limits.

## How it works

UI asks → `POST /chat/stream` → embed query → top-K chunks (MiniLM) → Cohere rerank → Groq answer with sources → SSE tokens.

## Run locally

```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # then fill in your keys!
uvicorn app.main:app --reload
```

- `GET /` — status · `GET /health` — chunks + rate-limit stats
- `POST /chat` — `{"message": "..."}` → answer + retrieved sources

## Env vars

| Var | Required | Default |
|---|---|---|
| `GROQ_API_KEY` | yes | — |
| `COHERE_API_KEY` | for rerank | — |
| `GROQ_MODEL` | no | `llama-3.3-70b-versatile` |
| `EMBEDDING_MODEL` | no | `all-MiniLM-L6-v2` |
| `TOP_K` | no | `3` |
| `ALLOWED_ORIGIN` | no | `http://localhost:5173` |

## Knowledge base

`data/*.md` auto-loads at startup (`about`, `experience`, `projects`, `skills`, `faq`). Edit + restart to update what the bot knows.

## Deploy

Render (set env vars in dashboard). Rate limits: per-IP per-min/day + global/day.
