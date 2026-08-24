from fastapi import FastAPI

from app.api.v1.router import api_router


app = FastAPI(
    title="AkaSphere API",
    description="AI-powered collaboration platform",
    version="0.1.0",
)


app.include_router(
    api_router,
    prefix="/api/v1",
)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "akasphere-api",
        "version": "0.1.0",
    }