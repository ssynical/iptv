from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="IPTV Backend",
    description="Xtream Codes Compatible IPTV Backend",
    version="1.0.0",
    debug=settings.debug
)

@app.get("/")
async def root():
    return {"message": "iptv backend running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}