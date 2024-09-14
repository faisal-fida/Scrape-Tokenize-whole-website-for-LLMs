import requests
import time
import functools


class RetrySession:
    def __init__(self, session):
        self.session = session

    # Custom Retry decorator with wait mechanism
    def retry(attempts: int, wait_time: int):
        def decorator_retry(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(attempts):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        print(f"Attempt {attempt + 1} failed: {e}")
                        if attempt < attempts - 1:
                            time.sleep(wait_time)
                        else:
                            raise

            return wrapper

        return decorator_retry

    @retry(attempts=3, wait_time=1)
    def fetch_with_retry(self, url: str) -> requests.Response:
        """Fetch the URL with retries."""
        response = self.session.get(url)
        response.raise_for_status()
        return response
