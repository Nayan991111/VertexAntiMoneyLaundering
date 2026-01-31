from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.config import Settings

# UPDATED: Importing all endpoints including Auth (Day 14) and Graph (Day 12)
from app.api.v1.endpoints import customers, transactions, analytics, reports, audit, graph, auth

settings = Settings()

# 1. INITIALIZE RATE LIMITER (Day 14 Security)
# Strategies: FixedWindow is default. Key: Remote IP Address.
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="VertexAntiMoneyLaundering Regulatory Compliance Engine API"
)

# 2. REGISTER LIMITER CORE
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 3. REGISTER ROUTERS
# --------------------------------------------------------------------------
# 1. Customers Router
app.include_router(customers.router, prefix="/api/v1/customers", tags=["customers"])

# 2. Transactions Router
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["transactions"])

# 3. Analytics Router (Day 7 Addition)
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])

# 4. Reports Router (Day 9 Addition - PDF Generation)
app.include_router(reports.router, prefix="/api/v1/reports", tags=["reports"])

# 5. Audit Router (Day 11 Addition - Immutable Log Viewer)
app.include_router(audit.router, prefix="/api/v1/audit", tags=["audit"])

# 6. Graph Router (Day 12 Addition - Neo4j Intelligence)
app.include_router(graph.router, prefix="/api/v1/graph", tags=["graph"])

# 7. Auth Router (Day 14 Addition - Security Token)
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
# CRITICAL: Mount at root for standard OAuth2 /token path
app.include_router(auth.router, tags=["auth"]) 
# --------------------------------------------------------------------------

@app.get("/")
@limiter.limit("5/minute") # SECURITY: Restrict probing to 5 requests/min
async def root(request: Request): # 'request' argument is REQUIRED for limiter
    return {
        "message": "Compliance Engine Active", 
        "status": "Green", 
        "security": "Rate Limiting Enabled",
        "version": settings.PROJECT_VERSION
    }