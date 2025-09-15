from fastapi import FastAPI
from app.config import settings
from app.database import connect_to_mongo, close_mongo_connection, get_database

app = FastAPI(
    title="IPTV Backend",
    description="Xtream Codes Compatible IPTV Backend",
    version="1.0.0",
    debug=settings.debug
)

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

@app.get("/")
async def root():
    return {"message": "iptv backend running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/db-test")
async def test_database():
    try:
        db = get_database()
        result = await db.command("ping")
        return {"database": "connected", "ping": result}
    except Exception as e:
        return {"database": "error", "message": str(e)}