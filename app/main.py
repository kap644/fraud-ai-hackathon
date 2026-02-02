
from fastapi import FastAPI
from app.routes.voice_detection import router as voice_router
from app.routes.honeypot import router as honeypot_router

app = FastAPI()

app.include_router(voice_router, prefix="/api/voice-detection")
app.include_router(honeypot_router, prefix="/api/honeypot")

@app.get("/")
def root():
    return {"status": "API running"}
