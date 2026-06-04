import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_check_returns_200(async_client: AsyncClient):
    response = await async_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "metrics" in data

@pytest.mark.asyncio
async def test_health_live_returns_200(async_client: AsyncClient):
    response = await async_client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "alive"

@pytest.mark.asyncio
async def test_start_test_invalid_url(async_client: AsyncClient):
    response = await async_client.post("/api/start", json={
        "url": "not-a-valid-url",
        "concurrency": 10
    })
    # Should fail pydantic validation
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_start_test_invalid_concurrency(async_client: AsyncClient):
    response = await async_client.post("/api/start", json={
        "url": "https://example.com",
        "concurrency": 1000000 # Over the limit
    })
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_start_test_valid_payload(async_client: AsyncClient):
    response = await async_client.post("/api/start", json={
        "url": "https://example.com",
        "concurrency": 10
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    
    # Clean up by stopping it
    await async_client.post("/api/stop")
