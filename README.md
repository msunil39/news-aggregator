# Smart News Aggregator

A small project I built to scrape tech news from multiple sources, clean duplicate entries, store them in SQLite, and expose the data through a FastAPI API.

### Features

* Scrapes headlines from multiple sources
* Cleans and removes duplicate articles
* Stores articles in SQLite
* FastAPI endpoints for retrieving data
* Basic unit tests and CI pipeline

### Project Structure

```
news-aggregator/
│
├── app/
│   ├── scraper.py
│   ├── cleaner.py
│   ├── database.py
│   └── main.py
│
├── tests/
├── requirements.txt
└── README.md
```

### Running the project

Clone the repository:

```bash
git clone <repo-url>
cd news-aggregator
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run API:

```bash
uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

### API Endpoints

```
GET    /
POST   /scrape
GET    /articles
GET    /stats
```

Example:

```bash
curl -X POST http://127.0.0.1:8000/scrape

curl http://127.0.0.1:8000/articles?limit=10
```

### Running Tests

```bash
pytest -v
```

### Tech Used

* Python
* FastAPI
* BeautifulSoup
* Pandas
* SQLite
* Pytest

### Why I Built This

I wanted to practice building an end-to-end data pipeline that includes scraping, cleaning, storage, APIs, testing, and basic automation in one project.
