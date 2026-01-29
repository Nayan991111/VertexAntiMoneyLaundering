from fastapi import FastAPI
from app.core.config import Settings
# FIXED: Added 'transactions' to the import
from app.api.v1.endpoints import customers, transactions 

settings = Settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="ZeTheta Regulatory Compliance Engine API"
)

# Include the Customers Router
app.include_router(customers.router, prefix="/api/v1/customers", tags=["customers"])

# FIXED: Registered the Transactions Router
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["transactions"])

@app.get("/")
async def root():
    return {"message": "Compliance Engine Active", "status": "Green"}