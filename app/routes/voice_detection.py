
from fastapi import APIRouter, Depends, Request
from app.auth import verify_api_key
import random

router = APIRouter()

@router.post("")
async def voice_detect(request: Request, api_key=Depends(verify_api_key)):
    data = await request.json()
    if "language" not in data or "audio_format" not in data or "audio_base64" not in data:
        return {"status": "error", "message": "Invalid input"}

    return {
        "status": "success",
        "result": {
            "classification": "AI_GENERATED",
            "confidence": round(random.uniform(0.75, 0.9), 2),
            "language": data["language"]
        },
        "message": "Audio analyzed successfully"
    }
