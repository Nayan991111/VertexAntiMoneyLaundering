from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="High-Frequency Regulatory Compliance System",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.get("/")
async def health_check():
    return {
        "system": "ZeTheta Compliance Engine",
        "status": "Operational",
        "clearance": "Top Secret"
    }