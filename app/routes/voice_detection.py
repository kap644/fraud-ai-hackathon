from fastapi import APIRouter, Depends, Request
from app.auth import verify_api_key
import base64
import os
import uuid

from app.audio_analysis import analyze_audio
from app.scoring import calculate_confidence
from app.decision import classify

router = APIRouter()

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

@router.post("")
async def voice_detect(request: Request, api_key=Depends(verify_api_key)):
    data = await request.json()

    language = data.get("language")
    audio_format = data.get("audio_format") or data.get("audioFormat")
    audio_base64 = (
        data.get("audio_base64")
        or data.get("audioBase64")
        or data.get("audio")
    )

    if not language or not audio_format or not audio_base64:
        return {"status": "error", "message": "Invalid input"}

    try:
        # ---------- Decode base64 ----------
        audio_bytes = base64.b64decode(audio_base64)

        file_name = f"{uuid.uuid4()}.{audio_format}"
        audio_path = os.path.join(TEMP_DIR, file_name)

        with open(audio_path, "wb") as f:
            f.write(audio_bytes)

        # ---------- Analyze audio ----------
        features = analyze_audio(audio_path)
        confidence = calculate_confidence(features)

        # ---------- 🔥 AI-VOICE HEURISTIC (VERY IMPORTANT) ----------
        # AI voices are too clean (low pitch variation)
        if features.get("pitch_variation", 0) < 8:
            label = "AI"
        else:
            label = classify(confidence)

        # ---------- Cleanup ----------
        os.remove(audio_path)

        return {
            "status": "success",
            "result": {
                "classification": label,
                "confidence": round(confidence, 2),
                "language": language
            },
            "analysis": features,
            "message": "Voice analyzed"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Processing failed: {str(e)}"
        }







