from fastapi import APIRouter, Depends, Request
from app.auth import verify_api_key
import base64
import os
import uuid

from app.audio_analysis import analyze_audio
from app.scoring import calculate_confidence

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
        or data.get("audio_base64_format")
        or data.get("audio")
    )

    if not language or not audio_format or not audio_base64:
        return {
            "status": "error",
            "message": "Invalid input"
        }

    try:
        # ---------- Decode base64 audio ----------
        audio_bytes = base64.b64decode(audio_base64)

        file_name = f"{uuid.uuid4()}.{audio_format}"
        audio_path = os.path.join(TEMP_DIR, file_name)

        with open(audio_path, "wb") as f:
            f.write(audio_bytes)

        # ---------- Analyze audio ----------
        features = analyze_audio(audio_path)
        confidence = calculate_confidence(features)

        # ---------- FINAL FRAUD-SAFE DECISION ----------
        # Default = AI (safe choice)
        label = "AI"

        # Strong human cues required
        if (
            features["pitch_variance"] > 60
            and features["energy_variance"] > 0.05
            and features["silence_ratio"] > 0.15
        ):
            label = "Human"
        elif confidence > 0.75:
            label = "Suspicious"

        # ---------- Cleanup ----------
        os.remove(audio_path)

        return {
            "status": "success",
            "result": {
                "classification": label,
                "confidence": confidence,
                "language": language
            },
            "analysis": features,
            "message": "Audio analyzed successfully"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Processing failed: {str(e)}"
        }




