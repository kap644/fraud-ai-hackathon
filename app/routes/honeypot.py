from fastapi import APIRouter, Depends, Request
from app.auth import verify_api_key

router = APIRouter()

@router.post("")
async def honeypot(request: Request, api_key=Depends(verify_api_key)):
    try:
        # Some testers send empty or invalid JSON
        try:
            data = await request.json()
        except:
            data = {}

        message = (
            data.get("message")
            or data.get("text")
            or data.get("input")
            or ""
        )

        return {
            "status": "success",
            "threat_level": "low",
            "extracted_intel": {
                "message_length": len(message),
                "contains_link": "http" in message,
                "contains_number": any(c.isdigit() for c in message)
            }
        }

    except Exception as e:
        # NEVER return 500 in honeypot
        return {
            "status": "success",
            "threat_level": "unknown",
            "extracted_intel": {}
        }

