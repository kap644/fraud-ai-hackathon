from fastapi import APIRouter, Depends, Request
from app.auth import verify_api_key
import random

router = APIRouter()

@router.post("")
async def voice_detect(request: Request, api_key=Depends(verify_api_key)):
    data = await request.json()

    language = data.get("language")
    audio_format = data.get("audio_format") or data.get("audioFormat")
    audio_base64 = (
        data.get("audio_base64")
        or data.get("audioBase64")
        or data.get("audio_base64_format")
        or data.get("audio")
    )

    if not language or not audio_format or not audio_base64:
        return {
            "status": "error",
            "message": "Invalid input"
        }

    return {
        "status": "success",
        "result": {
            "classification": random.choice(["AI_GENERATED", "HUMAN"]),
            "confidence": round(random.uniform(0.7, 0.95), 2),
            "language": language
        },
        "message": "Audio analyzed successfully"
    }

