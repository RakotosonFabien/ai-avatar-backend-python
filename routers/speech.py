from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
import os
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

router = APIRouter()
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

class SpeechRequest(BaseModel):
    text: str

@router.post("/speak")
def generate_speech(request: SpeechRequest):
    try:
        audio_stream = client.text_to_speech.stream(
            text=request.text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",  # Rachel (you can change it)
            model_id="eleven_multilingual_v2"
        )

        buffer = BytesIO()
        for chunk in audio_stream:
            if isinstance(chunk, bytes):
                buffer.write(chunk)

        buffer.seek(0)
        return StreamingResponse(buffer, media_type="audio/mpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
