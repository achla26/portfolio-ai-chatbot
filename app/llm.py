from groq import Groq
from app.config import GROQ_API_KEY, GROQ_MODEL
from app.prompt import SYSTEM_PROMPT, build_prompt

client = Groq(api_key=GROQ_API_KEY)


def generate_response(question: str, context: str) -> str:
    """Generate response using Groq LLM (non-streaming)"""
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


def generate_response_stream(question: str, context: str):
    """Generate streaming response using Groq LLM"""
    user_message = build_prompt(context, question)
    
    stream = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=800,
        stream=True,  # Enable streaming
    )
    
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content