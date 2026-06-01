import sqlite3
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

DB_PATH = os.getenv("DB_PATH", "news.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT    NOT NULL,
            url         TEXT    UNIQUE NOT NULL,
            source      TEXT    NOT NULL,
            scraped_at  TEXT    NOT NULL,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_source ON articles(source)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_scraped_at ON articles(scraped_at)")
    conn.commit()
    conn.close()
    logger.info("Database initialised")


def insert_articles(articles: list) -> int:
    """Insert articles, skip duplicates. Returns count of newly inserted rows."""
    conn = get_connection()
    inserted = 0
    for article in articles:
        try:
            conn.execute(
                """
                INSERT OR IGNORE INTO articles (title, url, source, scraped_at)
                VALUES (:title, :url, :source, :scraped_at)
                """,
                article,
            )
            if conn.execute("SELECT changes()").fetchone()[0]:
                inserted += 1
        except Exception as e:
            logger.error(f"Insert error: {e}")
    conn.commit()
    conn.close()
    logger.info(f"Inserted {inserted} new articles into DB")
    return inserted


def fetch_articles(source: str = None, limit: int = 50, offset: int = 0) -> list:
    conn = get_connection()
    if source:
        rows = conn.execute(
            "SELECT * FROM articles WHERE source = ? ORDER BY scraped_at DESC LIMIT ? OFFSET ?",
            (source, limit, offset),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM articles ORDER BY scraped_at DESC LIMIT ? OFFSET ?",
            (limit, offset),
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def fetch_stats() -> dict:
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
    by_source = conn.execute(
        "SELECT source, COUNT(*) as count FROM articles GROUP BY source"
    ).fetchall()
    conn.close()
    return {
        "total": total,
        "by_source": {row["source"]: row["count"] for row in by_source},
    }
