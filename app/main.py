from fastapi import FastAPI
from app.config import settings
from app.database import connect_to_mongo, close_mongo_connection, get_database
from app.api.auth import router as auth_router
from app.api.xtream import router as xtream_router
from app.api.admin import router as admin_router

app = FastAPI(
    title="IPTV Backend",
    description="Xtream Codes Compatible IPTV Backend",
    version="1.0.0",
    debug=settings.debug
)

app.include_router(auth_router)
app.include_router(xtream_router)
app.include_router(admin_router)

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