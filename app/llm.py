from groq import Groq, AsyncGroq
from app.config import GROQ_API_KEY, GROQ_MODEL
from app.prompt import SYSTEM_PROMPT, build_prompt

client = Groq(api_key=GROQ_API_KEY)

async_client = AsyncGroq(api_key=GROQ_API_KEY)  


def generate_response(question: str, context: str) -> str:
    """Non-streaming response"""
    user_message = build_prompt(context, question)
    
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=800,
    )
    
    return response.choices[0].message.content


async def generate_response_stream_async(question: str, context: str):
    """✅ Async streaming response using AsyncGroq"""
    user_message = build_prompt(context, question)
    
    stream = await async_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=800,
        stream=True,
    )
    
    async for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content


# Keep old sync version for backward compatibility
def generate_response_stream(question: str, context: str):
    """Sync streaming (fallback)"""
    user_message = build_prompt(context, question)
    
    stream = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=800,
        stream=True,
    )
    
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content