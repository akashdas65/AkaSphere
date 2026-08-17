from fastapi import FastAPI

app = FastAPI(
    title="AkaSphere API",
    description="AI-powered collaboration platform",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "akasphere-api",
        "version": "0.1.0",
    }