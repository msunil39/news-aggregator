import pytest
from app.cleaner import clean_title, deduplicate, clean_and_deduplicate


def test_clean_title_strips_whitespace():
    assert clean_title("  Hello   World  ") == "Hello World"


def test_clean_title_removes_extra_spaces():
    assert clean_title("Hello\n\tWorld") == "Hello World"


def test_deduplicate_removes_exact_url_duplicates():
    articles = [
        {"title": "Article One", "url": "https://example.com/1", "source": "Test", "scraped_at": "2024-01-01"},
        {"title": "Article One Again", "url": "https://example.com/1", "source": "Test", "scraped_at": "2024-01-01"},
    ]
    result = deduplicate(articles)
    assert len(result) == 1


def test_deduplicate_removes_similar_titles():
    articles = [
        {"title": "Python is great for data", "url": "https://a.com/1", "source": "A", "scraped_at": "2024-01-01"},
        {"title": "Python is great for data", "url": "https://b.com/2", "source": "B", "scraped_at": "2024-01-01"},
    ]
    result = deduplicate(articles)
    assert len(result) == 1


def test_deduplicate_keeps_unique_articles():
    articles = [
        {"title": "Python tips and tricks", "url": "https://a.com/1", "source": "A", "scraped_at": "2024-01-01"},
        {"title": "FastAPI tutorial for beginners", "url": "https://b.com/2", "source": "B", "scraped_at": "2024-01-01"},
        {"title": "Data engineering with DuckDB", "url": "https://c.com/3", "source": "C", "scraped_at": "2024-01-01"},
    ]
    result = deduplicate(articles)
    assert len(result) == 3


def test_clean_and_deduplicate_filters_empty():
    articles = [
        {"title": "", "url": "https://a.com/1", "source": "A", "scraped_at": "2024-01-01"},
        {"title": "Valid Article Title Here", "url": "https://b.com/2", "source": "B", "scraped_at": "2024-01-01"},
        {"title": "Another Valid Title", "url": "", "source": "C", "scraped_at": "2024-01-01"},
    ]
    result = clean_and_deduplicate(articles)
    assert len(result) == 1
    assert result[0]["title"] == "Valid Article Title Here"
