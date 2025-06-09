import os
import aiohttp
from config import GEMINI_API_KEY

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"

async def ask_llm(question: str) -> str:
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": question}]
            }
        ]
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
                headers=headers,
                json=payload
            ) as res:
                data = await res.json()

                # Check for errors
                if "candidates" not in data:
                    return f"❌ Gemini API Error: {data.get('error', {}).get('message', 'Unknown error')}"

                return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"❌ Internal Error: {str(e)}"
