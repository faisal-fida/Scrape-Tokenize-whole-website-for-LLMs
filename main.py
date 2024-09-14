from web_text_scraper.scraper import Scraper
from web_text_scraper.parser import SitemapParser

import os
import logging
import requests

logging.basicConfig(
    format="%(levelname)s, %(asctime)s, %(module)s:%(lineno)d, %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)


def save_to_file(file_base_name, content):
    base_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(base_dir, exist_ok=True)
    filepath = os.path.join(base_dir, f"{file_base_name}.txt")
    with open(filepath, "w") as f:
        f.writelines(content)
    logging.info(f"Saved extracted texts to {filepath}")


def process_sitemap(sitemap_url):
    session = requests.Session()

    try:
        parser = SitemapParser(sitemap_url, session)
        sitemap_links = parser.get_sitemap_links()
    except Exception as e:
        logging.error(f"Failed to fetch sitemap links: {e}")
        return

    try:
        scraper = Scraper(sitemap_url, session)
        texts = scraper.extract_texts_from_urls(sitemap_links)
    except Exception as e:
        logging.error(f"Failed to extract texts from links: {e}")
        return

    try:
        file_base_name = sitemap_url.split("/")[-2].split(".")[0]
        save_to_file(file_base_name, texts)
    except IndexError:
        save_to_file(f"sitemap_texts_{len(texts)}", texts)
    except Exception as e:
        logging.error(f"Failed to save extracted texts: {e}")
        return


if __name__ == "__main__":
    sitemap_url = "https://allfly.io/sitemap.xml"
    process_sitemap(sitemap_url)
