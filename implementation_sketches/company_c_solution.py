"""
Company C - API Gateway (HTTP/2 multiplexing + connection pools)
Pseudo-implementation sketch using asyncio and connection pools.
"""
import asyncio
from asyncio import Semaphore

class UpstreamClientPool:
    def __init__(self, max_concurrent_streams=100):
        self.semaphore = Semaphore(max_concurrent_streams)
    async def call(self, endpoint, payload, timeout=0.3):
        async with self.semaphore:
            # In real impl use HTTP/2 client library with connection reuse
            await asyncio.sleep(0.05)  # simulate network call
            return {"endpoint": endpoint, "data": 123}

# Global pools per service
pools = {
    "svc_a": UpstreamClientPool(max_concurrent_streams=200),
    "svc_b": UpstreamClientPool(max_concurrent_streams=200),
    "svc_c": UpstreamClientPool(max_concurrent_streams=200),
}

async def handle_request(req):
    # parallel fan-out with bounded concurrency
    tasks = []
    for svc in req.get("services", ["svc_a", "svc_b"]):
        pool = pools[svc]
        tasks.append(pool.call("/data", req.get("params", {})))
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    # aggregate responses
    aggregated = {}
    for r in responses:
        if isinstance(r, Exception):
            # handle failure / fallback
            continue
        aggregated.update(r)
    return aggregated

async def main():
    # Start server that receives requests and calls handle_request
    pass

if __name__ == "__main__":
    asyncio.run(main())
