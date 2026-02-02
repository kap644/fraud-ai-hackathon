
from fastapi import APIRouter, Depends
from app.auth import verify_api_key

router = APIRouter()

@router.post("")
def honeypot(data: dict, api_key=Depends(verify_api_key)):
    msg = data.get("message", "").lower()
    keywords = []

    if "click" in msg:
        keywords.append("click")
    if "prize" in msg or "lottery" in msg:
        keywords.append("prize")

    return {
        "status": "success",
        "threat_level": "HIGH" if keywords else "LOW",
        "scam_type": "Phishing" if keywords else "Safe",
        "keywords": keywords
    }
