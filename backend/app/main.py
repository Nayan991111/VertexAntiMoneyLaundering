from fastapi import FastAPI
from app.core.config import Settings
from app.api.v1.endpoints import customers

settings = Settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="ZeTheta Regulatory Compliance Engine API"
)

# Include the Customers Router
app.include_router(customers.router, prefix="/api/v1/customers", tags=["customers"])

@app.get("/")
async def root():
    return {"message": "Compliance Engine Active", "status": "Green"}