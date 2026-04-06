import time
from unittest.mock import MagicMock
from ghtopdep.prefetch import PagePrefetcher
from ghtopdep.rate_limiter import TokenBucketRateLimiter


def _make_mock_session(pages):
    """Create a mock session that returns canned HTML for each URL."""
    session = MagicMock()

    def fake_get(url):
        resp = MagicMock()
        resp.text = pages.get(url, "<html>not found</html>")
        return resp

    session.get.side_effect = fake_get
    return session


def test_get_without_submit_fetches_synchronously():
    """When no prefetch was submitted, get() fetches the URL directly."""
    session = _make_mock_session({"http://page1": "<html>page1</html>"})
    limiter = TokenBucketRateLimiter(rate=100, period=1.0)
    prefetcher = PagePrefetcher(session, limiter)

    result = prefetcher.get("http://page1")
    assert result == "<html>page1</html>"
    session.get.assert_called_once_with("http://page1")
    prefetcher.shutdown()


def test_submit_then_get_returns_prefetched():
    """Submit kicks off a background fetch; get() returns its result."""
    pages = {
        "http://page1": "<html>page1</html>",
        "http://page2": "<html>page2</html>",
    }
    session = _make_mock_session(pages)
    limiter = TokenBucketRateLimiter(rate=100, period=1.0)
    prefetcher = PagePrefetcher(session, limiter)

    prefetcher.submit("http://page2")
    # Give the background thread a moment
    time.sleep(0.1)
    result = prefetcher.get("http://page2")
    assert result == "<html>page2</html>"
    prefetcher.shutdown()


def test_submit_ignores_duplicate():
    """Calling submit twice without a get in between is a no-op."""
    pages = {"http://page1": "<html>page1</html>"}
    session = _make_mock_session(pages)
    limiter = TokenBucketRateLimiter(rate=100, period=1.0)
    prefetcher = PagePrefetcher(session, limiter)

    prefetcher.submit("http://page1")
    prefetcher.submit("http://page1")  # should be ignored
    time.sleep(0.1)
    result = prefetcher.get("http://page1")
    assert result == "<html>page1</html>"
    # session.get should only be called once (the first submit)
    session.get.assert_called_once_with("http://page1")
    prefetcher.shutdown()


def test_shutdown_is_safe_with_no_pending():
    """Shutdown without any pending work should not raise."""
    session = MagicMock()
    limiter = TokenBucketRateLimiter(rate=100, period=1.0)
    prefetcher = PagePrefetcher(session, limiter)
    prefetcher.shutdown()  # should not raise


def test_get_blocks_until_prefetch_completes():
    """get() should block if prefetch is still in progress."""
    def slow_get(url):
        time.sleep(0.3)
        resp = MagicMock()
        resp.text = "<html>slow</html>"
        return resp

    session = MagicMock()
    session.get.side_effect = slow_get
    limiter = TokenBucketRateLimiter(rate=100, period=1.0)
    prefetcher = PagePrefetcher(session, limiter)

    prefetcher.submit("http://slow-page")
    start = time.monotonic()
    result = prefetcher.get("http://slow-page")
    elapsed = time.monotonic() - start

    assert result == "<html>slow</html>"
    assert elapsed >= 0.2, "get() should have blocked waiting for the slow fetch"
    prefetcher.shutdown()
