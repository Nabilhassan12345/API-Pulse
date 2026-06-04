import asyncio
import aiohttp
import time
from typing import Dict, Any, List
from core.logger import logger
from schemas.scenario import Scenario, ScenarioStep
import re

class LoadTester:
    def __init__(self):
        self.is_running = False
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "current_rps": 0,
            "average_latency_ms": 0.0,
            "active_connections": 0
        }
        self.latencies = []
        self._start_time = 0
        self._task = None

    async def _make_request(self, session: aiohttp.ClientSession, step: ScenarioStep, context: Dict[str, Any]):
        url = step.url
        # Simulate dynamic variable injection
        for key, val in context.items():
            url = url.replace(f"{{{{{key}}}}}", str(val))
            
        start_time = time.time()
        try:
            async with session.request(step.method, url, headers=step.headers, json=step.payload) as response:
                await response.read()
                latency = (time.time() - start_time) * 1000
                self.stats["successful_requests"] += 1
                
                # Mock variable extraction
                if step.extract_vars and response.status == 200:
                    try:
                        data = await response.json()
                        for var_name, json_path in step.extract_vars.items():
                            context[var_name] = data.get(json_path.replace("$.", "")) # Simplified mock extraction
                    except Exception:
                        pass
        except Exception:
            latency = (time.time() - start_time) * 1000
            self.stats["failed_requests"] += 1

        self.stats["total_requests"] += 1
        
        # Calculate moving average
        n = self.stats["total_requests"]
        old_avg = self.stats["average_latency_ms"]
        self.stats["average_latency_ms"] = old_avg + (latency - old_avg) / n

    async def _worker(self, scenario: Scenario):
        async with aiohttp.ClientSession() as session:
            self.stats["active_connections"] += 1
            try:
                while self.is_running:
                    context = {}
                    for step in scenario.steps:
                        if not self.is_running:
                            break
                        await self._make_request(session, step, context)
                        if step.think_time_ms > 0:
                            await asyncio.sleep(step.think_time_ms / 1000.0)
            finally:
                self.stats["active_connections"] -= 1

    async def _run_test(self, scenario: Scenario):
        tasks = []
        for _ in range(scenario.concurrency):
            tasks.append(asyncio.create_task(self._worker(scenario)))
            
        start_time = time.time()
        while self.is_running:
            await asyncio.sleep(1)
            elapsed = time.time() - start_time
            self.stats["current_rps"] = round(self.stats["total_requests"] / elapsed, 2)
            
            # Auto-stop based on duration
            if scenario.duration_seconds and elapsed >= scenario.duration_seconds:
                self.stop()
                
        await asyncio.gather(*tasks)

    def start(self, scenario: Scenario):
        if not self.is_running:
            logger.info("Starting distributed scenario test", extra={"scenario": scenario.name, "concurrency": scenario.concurrency})
            # Reset stats
            self.stats = {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "current_rps": 0,
                "average_latency_ms": 0.0,
                "active_connections": 0
            }
            self.is_running = True
            self._task = asyncio.create_task(self._run_test(scenario))

    def stop(self):
        logger.info("Stopping load test", extra={"final_stats": self.stats})
        self.is_running = False

    def get_stats(self) -> Dict[str, Any]:
        return self.stats

load_tester = LoadTester()
