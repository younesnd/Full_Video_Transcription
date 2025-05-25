import aiohttp
import aiofiles
import os
from dotenv import load_dotenv

load_dotenv()
api_key = "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"

async def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe audio using Groq's Whisper API.
    """
    url = "https://api.groq.com/openai/v1/audio/transcriptions"

    try:
        async with aiofiles.open(audio_path, 'rb') as audio_file:
            audio_data = await audio_file.read()

        data = aiohttp.FormData()
        data.add_field('file', audio_data, filename='audio.wav', content_type='audio/wav')
        data.add_field('model', 'whisper-large-v3')
        data.add_field('response_format', 'json')

        headers = {
            "Authorization": f"Bearer {api_key}"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Whisper API failed: {error_text}")

                result = await response.json()
                return result["text"]

    except Exception as e:
        raise
