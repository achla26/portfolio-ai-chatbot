import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from app import rag, llm
from app.config import ALLOWED_ORIGIN
from app.rate_limiter import rate_limiter

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize RAG on server start"""
    rag.initialize_rag()
    print("✅ Rate limiter initialized")
    print(f"   Limits: {rate_limiter.per_minute}/min, {rate_limiter.per_day}/day per IP")
    print(f"   Global limit: {rate_limiter.global_per_day}/day")
    yield
    # Shutdown logic 

app = FastAPI(title="Portfolio AI Backend" , lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)


class ChatResponse(BaseModel):
    answer: str
    retrieved: list


@app.get("/")
async def root():
    return {"status": "ok", "message": "Portfolio AI Backend running"}


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "chunks": len(rag.chunks),
        "rate_limit_stats": rate_limiter.get_stats()
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, http_request: Request):
    # Rate limit check
    rate_limiter.check_rate_limit(http_request)
    
    try:
        context, retrieved = rag.get_context(request.message)
        answer = llm.generate_response(request.message, context)
        
        return ChatResponse(
            answer=answer,
            retrieved=[
                {
                    "source": r["source"],
                    "score": r["score"],
                    "preview": r["text"][:150] + "..."
                }
                for r in retrieved
            ]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Streaming endpoint
@app.post("/chat/stream")
async def chat_stream(request: ChatRequest, http_request: Request):
    """Stream response using Server-Sent Events (SSE) - Async version"""
    import asyncio
    
    # Rate limit check
    rate_limiter.check_rate_limit(http_request)
    
    try:
        context, retrieved = rag.get_context(request.message)
        
        retrieved_formatted = [
            {
                "source": r["source"],
                "score": r["score"],
                "preview": r["text"][:150] + "..."
            }
            for r in retrieved
        ]
        
        async def event_generator():
            # 1. Send sources first
            yield f"data: {json.dumps({'type': 'sources', 'data': retrieved_formatted})}\n\n"
            await asyncio.sleep(0.01)  # ✅ Flush buffer
            
            # 2. Stream tokens (async!)
            async for token in llm.generate_response_stream_async(request.message, context):
                data = json.dumps({'type': 'token', 'data': token})
                yield f"data: {data}\n\n"
                await asyncio.sleep(0)  # ✅ Yield control to flush
            
            # 3. Send done signal
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
        
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache, no-transform",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
                "Content-Type": "text/event-stream",
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Admin endpoint (protect this in production!)
@app.get("/admin/stats")
async def admin_stats():
    """Get rate limiter stats"""
    return rate_limiter.get_stats()