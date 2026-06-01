import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SOURCES = [
    {
        "name": "Hacker News",
        "url": "https://news.ycombinator.com/",
        "item_selector": ".athing",
        "title_selector": ".titleline a",
        "link_attr": "href",
    },
    {
        "name": "Reuters Tech",
        "url": "https://www.reuters.com/technology/",
        "item_selector": "a[data-testid='Heading']",
        "title_selector": None,
        "link_attr": "href",
    },
    {
        "name": "Dev.to",
        "url": "https://dev.to/",
        "item_selector": "h2.crayons-story__title a",
        "title_selector": None,
        "link_attr": "href",
    },
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def scrape_source(source: dict) -> list:
    articles = []
    try:
        response = requests.get(source["url"], headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select(source["item_selector"])

        for item in items[:20]:
            if source["title_selector"]:
                title_el = item.select_one(source["title_selector"])
                title = title_el.get_text(strip=True) if title_el else None
                link = title_el.get(source["link_attr"], "") if title_el else ""
            else:
                title = item.get_text(strip=True)
                link = item.get(source["link_attr"], "")

            if not title or len(title) < 10:
                continue

            if link and link.startswith("/"):
                from urllib.parse import urlparse
                base = urlparse(source["url"])
                link = f"{base.scheme}://{base.netloc}{link}"

            articles.append({
                "title": title,
                "url": link,
                "source": source["name"],
                "scraped_at": datetime.utcnow().isoformat(),
            })

        logger.info(f"Scraped {len(articles)} articles from {source['name']}")

    except Exception as e:
        logger.error(f"Failed to scrape {source['name']}: {e}")

    return articles


def scrape_all() -> list:
    all_articles = []
    for source in SOURCES:
        articles = scrape_source(source)
        all_articles.extend(articles)
    logger.info(f"Total articles scraped: {len(all_articles)}")
    return all_articles
