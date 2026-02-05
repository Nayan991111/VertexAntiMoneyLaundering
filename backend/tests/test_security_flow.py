import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

# Constants
BASE_URL = "http://test"

@pytest.mark.asyncio
async def test_health_check_rate_limit():
    """
    Day 14 Objective: Verify Rate Limiting protects the system.
    """
    # FIX: Use ASGITransport to wrap the FastAPI app
    transport = ASGITransport(app=app)
    
    async with AsyncClient(transport=transport, base_url=BASE_URL) as ac:
        # Hit 1-5 (Allowed)
        for i in range(5):
            response = await ac.get("/")
            assert response.status_code == 200, f"Request {i+1} failed"
        
        # Hit 6 (Blocked)
        response = await ac.get("/")
        assert response.status_code == 429, "Rate Limit Failed: Did not block 6th request"
        print("\n[SUCCESS] Rate Limit Shield holds at 5 requests/min.")

@pytest.mark.asyncio
async def test_auth_workflow():
    """
    Day 14 Objective: Verify JWT Authentication Flow.
    """
    transport = ASGITransport(app=app)
    
    async with AsyncClient(transport=transport, base_url=BASE_URL) as ac:
        # 1. Login to get Token
        login_data = {
            "username": "nayan",
            "password": "secret"
        }
        response = await ac.post("/token", data=login_data)
        assert response.status_code == 200
        token = response.json()["access_token"]
        assert token is not None
        print(f"\n[SUCCESS] Authentication Token acquired: {token[:10]}...")

        # 2. Attempt Protected Action (Generate SAR)
        # We use headers to pass the token
        headers = {"Authorization": f"Bearer {token}"}
        
        # Hitting index 999 to verify we get past Auth (logic error 404) 
        # instead of Auth error (401)
        response = await ac.post("/api/v1/reports/generate_sar/999", headers=headers)
        
        # 404 means "Authorized, but ring not found" -> SUCCESS
        # 401 means "Get out" -> FAIL
        assert response.status_code != 401, "Auth Failed: Token rejected"
        assert response.status_code == 404, "Logic Error: Should have returned 404 for missing ring"
        print("[SUCCESS] Authorized Access to SAR Generator confirmed.")

@pytest.mark.asyncio
async def test_unauthorized_access():
    """
    Day 14 Objective: Verify Unauthenticated users are rejected.
    """
    transport = ASGITransport(app=app)
    
    async with AsyncClient(transport=transport, base_url=BASE_URL) as ac:
        # Attempt without header
        response = await ac.post("/api/v1/reports/generate_sar/1")
        assert response.status_code == 401
        print("[SUCCESS] Unauthorized request successfully rejected.")