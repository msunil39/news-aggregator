import pandas as pd
import re
import logging

logger = logging.getLogger(__name__)


def clean_title(title: str) -> str:
    """Normalize whitespace, strip HTML artifacts."""
    title = re.sub(r'\s+', ' ', title).strip()
    title = re.sub(r'[^\x20-\x7E]', '', title)
    return title


def deduplicate(articles: list) -> list:
    """
    Remove duplicate articles.
    Dedup strategy:
      1. Exact URL match
      2. Near-identical titles (lowercased, punctuation stripped)
    """
    if not articles:
        return []

    df = pd.DataFrame(articles)
    df["title"] = df["title"].apply(clean_title)
    df["title_key"] = (
        df["title"]
        .str.lower()
        .str.replace(r'[^a-z0-9 ]', '', regex=True)
        .str.strip()
    )

    before = len(df)

    df = df.drop_duplicates(subset=["url"], keep="first")

    df = df.drop_duplicates(subset=["title_key"], keep="first")

    df = df.drop(columns=["title_key"])

    after = len(df)
    logger.info(f"Deduplicated: {before} -> {after} articles ({before - after} removed)")

    return df.to_dict(orient="records")


def clean_and_deduplicate(articles: list) -> list:
    """Full cleaning pipeline."""
    articles = [a for a in articles if a.get("title") and a.get("url")]
    return deduplicate(articles)
