import requests
from bs4 import BeautifulSoup as Soup

from web_text_scraper.utils import RetrySession


class SitemapParser(RetrySession):
    def __init__(self, sitemap_url: str, session: requests.Session):
        super().__init__(session)
        self.url = sitemap_url
        self.sitemap_links = []
        self.sitemap_attrs = ["loc", "lastmod", "priority"]

    def get_sitemap_links(self) -> list:
        """Fetch the sitemap content and return a list of URLs found in it."""
        content = self.fetch_with_retry(self.url).content

        if not content:
            return []

        soup = Soup(content, "xml")
        urls = [url.get_text(strip=True) for url in soup.find_all("loc")]
        return urls
