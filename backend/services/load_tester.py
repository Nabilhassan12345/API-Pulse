import asyncio
import aiohttp
import time
from typing import Dict, Any
from core.logger import logger

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

    async def _worker(self, session: aiohttp.ClientSession, url: str):
        while self.is_running:
            start_req = time.time()
            self.stats["active_connections"] += 1
            try:
                async with session.get(url, timeout=5) as response:
                    await response.read()
                    if response.status < 400:
                        self.stats["successful_requests"] += 1
                    else:
                        self.stats["failed_requests"] += 1
            except Exception:
                self.stats["failed_requests"] += 1
            finally:
                self.stats["active_connections"] -= 1
                latency = (time.time() - start_req) * 1000
                self.latencies.append(latency)
                self.stats["total_requests"] += 1
                
                # Keep only last 100 latencies for moving average
                if len(self.latencies) > 100:
                    self.latencies.pop(0)

    async def _run_test(self, url: str, concurrency: int):
        self._start_time = time.time()
        self.is_running = True
        
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(self._worker(session, url)) for _ in range(concurrency)]
            
            # Monitoring loop
            while self.is_running:
                await asyncio.sleep(1)
                
                # Calculate RPS
                elapsed = time.time() - self._start_time
                if elapsed > 0:
                    self.stats["current_rps"] = int(self.stats["total_requests"] / elapsed)
                    
                # Calculate Average Latency
                if self.latencies:
                    self.stats["average_latency_ms"] = round(sum(self.latencies) / len(self.latencies), 2)
                    
            # Cancel all workers when stopping
            for t in tasks:
                t.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)

    def start(self, url: str, concurrency: int):
        if not self.is_running:
            logger.info("Starting load test", extra={"url": url, "concurrency": concurrency})
            # Reset stats
            self.stats = {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "current_rps": 0,
                "average_latency_ms": 0.0,
                "active_connections": 0
            }
            self.latencies = []
            self._task = asyncio.create_task(self._run_test(url, concurrency))

    def stop(self):
        logger.info("Stopping load test", extra={"final_stats": self.stats})
        self.is_running = False

    def get_stats(self) -> Dict[str, Any]:
        return self.stats

load_tester = LoadTester()
