import re
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup

from web_text_scraper.utils import RetrySession


class Scraper(RetrySession):
    def __init__(self, sitemap_url: str, session: requests.Session):
        super().__init__(session)
        self.sitemap_url = sitemap_url

    def clean_text(self, text: str) -> str:
        """Clean the extracted text."""
        # Remove non-ASCII, URLs, and extra newlines and spaces
        pattern = r"[^\x00-\x7F]+|https?://\S+|\n{3,}|\s{2,}"
        text = re.sub(pattern, " ", text)
        text = "\n".join(line for line in text.splitlines() if len(line.split()) >= 5)
        return text.strip()

    def extract_text_from_url(self, url: str) -> str:
        """Fetch and extract text from a single URL."""
        try:
            response = self.fetch_with_retry(url)
            soup = BeautifulSoup(response.content, "html.parser")
            soup_body = soup.find("body")
            if soup_body:
                text = soup_body.get_text(separator="\n", strip=True)
            else:
                text = soup.get_text(separator="\n", strip=True)

            text = self.clean_text(text)
            text = "Text extracted from " + url + "\n" + text + "\n\n"
            return text
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching URL {url.split("/")[-1][:10]}: {e}")
            return ""

    def extract_texts_from_urls(self, urls: list) -> list:
        logging.info("Starting extraction from multiple URLs")
        all_texts = []
        time_start = time.time()

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {
                executor.submit(self.extract_text_from_url, url): url for url in urls
            }
            for future in as_completed(futures):
                url = futures[future]
                try:
                    result = future.result()
                    all_texts.append(result)
                    logging.info(
                        f"Successfully processed URL: {url.split("/")[-1][:10]}"
                    )
                except Exception as e:
                    logging.error(
                        f"Error processing URL {url.split("/")[-1][:10]}: {e}"
                    )

        logging.info("Completed extraction from multiple URLs")
        logging.info(
            f"Time taken: {time.time() - time_start:.2f} seconds to scrape {len(all_texts)} URLs"
        )
        return all_texts
