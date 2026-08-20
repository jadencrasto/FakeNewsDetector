import requests
from bs4 import BeautifulSoup


class WebFetcher:

    def __init__(self, timeout=10):
        self.timeout = timeout

    def fetch(self, url):
        try:
            response = requests.get(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/151.0.0.0 Safari/537.36"
                )
            },
            timeout=10
        )

            if response.status_code != 200:
                return {
                    "status_code": response.status_code,
                    "url": url,
                    "text": "",
                    "error": f"HTTP {response.status_code}"
                }

            # Your existing HTML extraction code goes here
            soup = BeautifulSoup(response.text, "html.parser")

            for element in soup([
                "script",
                "style",
                "noscript"
            ]):
                element.decompose()

            text = soup.get_text(
                separator=" ",
                strip=True
            )

            return {
                "status_code": response.status_code,
                "url": response.url,
                "text": text,
                "error": None
            }

        except requests.RequestException as e:
            return {
                "status_code": 0,
                "url": url,
                "text": "",
                "error": str(e)
        }