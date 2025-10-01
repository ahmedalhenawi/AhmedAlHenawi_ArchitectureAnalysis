Performance Calculations and Assumptions
=========================================

General Notes:
- All calculations use values from the task description.
- Where ambiguous, reasonable assumptions are documented.
- Units: seconds (s), milliseconds (ms).

Company A (Real-time Chat)
--------------------------
Input:
- WebSocket connections: 10,000
- Messages per connection: 1 - 2 per minute (assume 1.5)
- Message size: <1KB
- CPU-bound fraction: 20%; I/O-bound: 80%
- Server: 8 cores
- App memory: 0.5 GB per process

Calculations:
- Messages/sec = 10,000 * 1.5 / 60 = 250 msg/s
- If CPU time per message = 5 ms -> CPU cores required = 250 * 0.005 = 1.25 cores
- If CPU time per message = 20 ms -> CPU cores required = 250 * 0.02 = 5 cores
- Running 8 processes (1 per core) uses ~8 * 0.5 = 4 GB app memory (plus OS)

Notes:
- DB latency (10-200ms) will dominate end-to-end latency unless cached or batched.
- Offload CPU-heavy tasks to avoid blocking event loop.

Company B (Image Processing)
---------------------------
Input:
- Avg image size: 5 MB
- Processing time: 2 - 10 s (assume 6s avg)
- Concurrent uploads typical: 50
- Memory per image: 2 GB
- Server: 16 cores, GPU acceleration

Calculations:
- Memory required for 50 concurrent = 50 * 2 GB = 100 GB
- If server has 64 GB => max concurrent by memory = floor(64 / 2) = 32
- If using 16 workers and avg processing 6s -> throughput = 16 / 6 ≈ 2.67 images/sec

Notes:
- Memory, not CPU, is bottleneck for concurrency here.
- Use queue/backpressure and autoscaling to handle bursts.

Company C (E-commerce API Gateway)
---------------------------------
Input:
- RPS = 1,000
- Fan-out per request = assume 4 services
- Avg upstream latency = 100 - 500 ms (assume 300 ms)
- Server: 4 cores
- CPU-bound fraction: 30%; I/O-bound: 70%

Calculations:
- Outstanding upstream calls = RPS * avg_latency * fanout
  = 1000 * 0.3 * 4 = 1,200 concurrent upstream calls
- If CPU time per request = 5 ms -> CPU cores needed = 1000 * 0.005 = 5 cores
- Peak (5x load): RPS = 5,000 -> Outstanding upstream calls = 5,000 * 0.3 * 4 = 6,000

Notes:
- On a 4-core box, sustaining 1,000 RPS depends on very low CPU time per request (<=4ms).
- Multiplexing and connection reuse plus caching reduce network overhead and reduce latency.

Sensitivity and Recommendations
-------------------------------
- Company A: if CPU time grows >20ms per message, increase number of worker processes or offload more work.
- Company B: scale horizontally or reduce memory footprint per job (streaming, chunking).
- Company C: employ caching at gateway, tune connection pools, and autoscale for spikes.

