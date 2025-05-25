import aiohttp
import os
from dotenv import load_dotenv

load_dotenv('/app/.env')

api_key = "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"


async def translate_text(text: str, target_language: str) -> str:
    """
    Translate the given text into the specified target language using Groq's LLaMA model.
    The translation should be exact and contain no extra annotations or explanations.
    """

    system_message = {
        "role": "system",
        "content": (
            "You are a translation assistant. "
            "Translate the user's input text exactly into the target language. "
            "Return only the translated text without adding any explanations, notes, or formatting."
        )
    }

    user_message = {
        "role": "user",
        "content": f"Translate the following text into {target_language}:\n\n{text}"
    }

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [system_message, user_message],
        "temperature": 0.0,  # deterministic output for exact translation
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status != 200:
                    error_text = await response.text()
                    return text

                result = await response.json()

                if "choices" not in result or not result["choices"]:
                    return text

                translation = result["choices"][0]["message"]["content"].strip()

                return translation

    except Exception:
        return text
