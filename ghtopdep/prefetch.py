from concurrent.futures import ThreadPoolExecutor


class PagePrefetcher:
    """Threaded single-page-ahead prefetcher.

    Fetches the next page in a background thread while the main
    thread processes the current page.

    Args:
        session: requests.Session (thread-safe).
        limiter: TokenBucketRateLimiter (thread-safe via lock).
    """

    def __init__(self, session, limiter):
        self._session = session
        self._limiter = limiter
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._pending = None

    def submit(self, url):
        """Start fetching url in a background thread.

        Only one prefetch at a time. If a prefetch is already
        pending, this call is a no-op.
        """
        if self._pending is not None:
            return
        self._pending = self._executor.submit(self._fetch, url)

    def get(self, url):
        """Return prefetched result if available, or fetch url synchronously.

        The caller must ensure get() is called for the same URL that
        was submitted. The url param is only used for the synchronous
        fallback path (no pending prefetch).
        """
        if self._pending is not None:
            result = self._pending.result()
            self._pending = None
            return result
        return self._fetch(url)

    def shutdown(self):
        """Cancel any pending prefetch and shut down the thread pool."""
        if self._pending is not None:
            self._pending.cancel()
        self._executor.shutdown(wait=False)

    def _fetch(self, url):
        self._limiter.acquire()
        response = self._session.get(url)
        return response.text
