import pytest
import sqlite3


@pytest.fixture()
def db_module(tmp_path, monkeypatch):
    db_path = str(tmp_path / "test.db")
    monkeypatch.setenv("DB_PATH", db_path)
    import importlib, app.database as m
    importlib.reload(m)
    m.init_db()
    return m


def test_init_creates_table(db_module, tmp_path):
    db_path = str(tmp_path / "test.db")
    conn = sqlite3.connect(db_path)
    tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    assert "articles" in tables
    conn.close()


def test_insert_and_fetch(db_module):
    articles = [{"title": "Test Article", "url": "https://test.com/1", "source": "Src", "scraped_at": "2024-01-01T00:00:00"}]
    inserted = db_module.insert_articles(articles)
    assert inserted == 1
    results = db_module.fetch_articles()
    assert len(results) == 1
    assert results[0]["title"] == "Test Article"


def test_insert_ignores_duplicates(db_module):
    article = {"title": "Dup", "url": "https://dup.com/1", "source": "S", "scraped_at": "2024-01-01T00:00:00"}
    db_module.insert_articles([article])
    second = db_module.insert_articles([article])
    assert second == 0


def test_stats(db_module):
    articles = [
        {"title": "A1", "url": "https://x.com/1", "source": "SrcA", "scraped_at": "2024-01-01T00:00:00"},
        {"title": "A2", "url": "https://x.com/2", "source": "SrcA", "scraped_at": "2024-01-01T00:00:00"},
        {"title": "B1", "url": "https://x.com/3", "source": "SrcB", "scraped_at": "2024-01-01T00:00:00"},
    ]
    db_module.insert_articles(articles)
    stats = db_module.fetch_stats()
    assert stats["total"] == 3
    assert stats["by_source"]["SrcA"] == 2
    assert stats["by_source"]["SrcB"] == 1
