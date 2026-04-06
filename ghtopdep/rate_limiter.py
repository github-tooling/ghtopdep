import threading
import time


class TokenBucketRateLimiter:
    """Synchronous, thread-safe token bucket rate limiter.

    Args:
        rate: Maximum requests allowed per period.
        period: Time period in seconds.
    """

    def __init__(self, rate, period):
        self._rate = rate
        self._period = period
        self._tokens = float(rate)
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def acquire(self):
        """Block until a token is available, then consume it."""
        with self._lock:
            self._refill()
            if self._tokens < 1.0:
                wait_time = (1.0 - self._tokens) * (self._period / self._rate)
                time.sleep(wait_time)
                self._refill()
            self._tokens -= 1.0

    def _refill(self):
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(
            float(self._rate),
            self._tokens + elapsed * (self._rate / self._period),
        )
        self._last_refill = now
