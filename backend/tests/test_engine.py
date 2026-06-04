import pytest
import asyncio
from services.load_tester import LoadTester

def test_load_tester_initialization():
    tester = LoadTester()
    assert not tester.is_running
    stats = tester.get_stats()
    assert stats["total_requests"] == 0
    assert stats["successful_requests"] == 0
    assert stats["failed_requests"] == 0
    assert stats["current_rps"] == 0

@pytest.mark.asyncio
async def test_get_stats_returns_zeroed_schema_before_start():
    tester = LoadTester()
    stats = tester.get_stats()
    assert stats["average_latency_ms"] == 0.0
    assert stats["active_connections"] == 0
