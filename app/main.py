from fastapi import FastAPI, Query, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
from app.scraper import scrape_all
from app.cleaner import clean_and_deduplicate
from app.database import init_db, insert_articles, fetch_articles, fetch_stats
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Smart News Aggregator API",
    description="Scrapes, deduplicates and serves tech news from multiple sources.",
    version="1.0.0",
)


@app.on_event("startup")
def startup():
    init_db()


class Article(BaseModel):
    id: int
    title: str
    url: str
    source: str
    scraped_at: str
    created_at: str


class ScrapeResult(BaseModel):
    scraped: int
    inserted: int
    message: str


class Stats(BaseModel):
    total: int
    by_source: dict


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "News Aggregator API is running"}


@app.post("/scrape", response_model=ScrapeResult, tags=["Pipeline"])
def run_scrape(background_tasks: BackgroundTasks):
    """
    Trigger a full scrape -> clean -> store pipeline run.
    """
    raw = scrape_all()
    clean = clean_and_deduplicate(raw)
    inserted = insert_articles(clean)
    return ScrapeResult(
        scraped=len(raw),
        inserted=inserted,
        message=f"Pipeline complete. {inserted} new articles stored.",
    )


@app.get("/articles", response_model=list[Article], tags=["Articles"])
def get_articles(
    source: Optional[str] = Query(None, description="Filter by source name"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """
    Retrieve articles with optional source filter and pagination.
    """
    articles = fetch_articles(source=source, limit=limit, offset=offset)
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found")
    return articles


@app.get("/stats", response_model=Stats, tags=["Analytics"])
def get_stats():
    """
    Return total article count and breakdown by source.
    """
    return fetch_stats()
