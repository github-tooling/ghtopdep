import time
import threading
from ghtopdep.rate_limiter import TokenBucketRateLimiter


def test_acquire_consumes_token():
    """First acquire should succeed instantly when bucket is full."""
    limiter = TokenBucketRateLimiter(rate=10, period=1.0)
    start = time.monotonic()
    limiter.acquire()
    elapsed = time.monotonic() - start
    assert elapsed < 0.1, "First acquire should be near-instant"


def test_acquire_blocks_when_empty():
    """After exhausting tokens, acquire should block until refill."""
    limiter = TokenBucketRateLimiter(rate=2, period=1.0)
    limiter.acquire()
    limiter.acquire()
    # Bucket is now empty; next acquire should block ~0.5s (1 token / 2 per sec)
    start = time.monotonic()
    limiter.acquire()
    elapsed = time.monotonic() - start
    assert 0.3 < elapsed < 1.0, "Should block ~0.5s waiting for refill"


def test_burst_up_to_rate():
    """Should allow a burst of 'rate' requests without blocking."""
    limiter = TokenBucketRateLimiter(rate=5, period=1.0)
    start = time.monotonic()
    for _ in range(5):
        limiter.acquire()
    elapsed = time.monotonic() - start
    assert elapsed < 0.2, "Burst of 5 should complete near-instantly"


def test_thread_safety():
    """Multiple threads calling acquire should not overshoot the rate."""
    limiter = TokenBucketRateLimiter(rate=4, period=1.0)
    results = []

    def worker():
        limiter.acquire()
        results.append(time.monotonic())

    threads = [threading.Thread(target=worker) for _ in range(6)]
    start = time.monotonic()
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=5)

    # 4 should complete near-instantly, remaining 2 should be delayed
    assert len(results) == 6
    fast = [r for r in results if r - start < 0.2]
    assert len(fast) == 4, "Exactly 4 tokens should be available immediately"
