# 🧠 Healthy dwelling

A dark, editorial-style psychology & neuroscience blog — Flask + Neon PostgreSQL, now powered by SQLAlchemy ORM with Adapter + Repository + Unit of Work patterns.

---

## Architecture

```
minds_mysteries/
├── app.py                  # Flask app factory
├── config.py               # Config (reads .env)
├── adapters/
│   ├── __init__.py         # Factory → get_adapter()
│   ├── base_adapter.py     # Abstract interface (ABC)
│   ├── orm_models.py       # SQLAlchemy ORM entities
│   ├── repositories.py     # Query repositories
│   ├── unit_of_work.py     # Request-scoped UoW/session
│   └── postgres_adapter.py # Adapter facade over repositories
├── routes/
│   └── blog.py             # All URL routes + JSON API
├── templates/              # Jinja2 templates
│   ├── base.html
│   ├── index.html
│   ├── blog.html
│   ├── article.html
│   ├── categories.html
│   ├── search.html
│   ├── _article_card.html  # Reusable card partial
│   └── _sidebar.html       # Reusable sidebar partial
├── static/
│   ├── css/style.css
│   └── js/main.js
├── schema.sql              # DB schema (run once)
├── seed.py                 # Sample content seeder
└── requirements.txt
```

## Data Access Patterns

The app keeps route/template code database-agnostic via these layers:

- Adapter: app talks only to `BaseAdapter`
- Repository: query logic is isolated in repository classes
- Unit of Work: one request-scoped SQLAlchemy session with commit/rollback behavior

This preserves clean boundaries while still using ORM models.

```
Application → get_adapter() → BaseAdapter (interface)
                                    ↑
                          PostgreSQLAdapter  ←  Neon DB
                          MySQLAdapter       ←  future
                          MockAdapter        ←  testing
```

**To swap the database:**
1. Create `adapters/my_db_adapter.py` implementing `BaseAdapter`
2. Register it in `adapters/__init__.py`:
   ```python
   ADAPTER_REGISTRY = {
       "postgres": PostgreSQLAdapter,
       "mydb":     MyDbAdapter,   # ← add this
   }
   ```
3. Set `DB_ADAPTER=mydb` in `.env`

---

## Setup

### 1. Install dependencies

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file (or export vars):

```env
DATABASE_URL=postgresql://neondb_owner:<password>@<host>/neondb?sslmode=require&channel_binding=require
SECRET_KEY=replace-with-a-long-random-secret
DB_ADAPTER=postgres
DEBUG=True
APP_HOST=0.0.0.0
APP_PORT=5001
ARTICLES_PER_PAGE=9
```

`DATABASE_URL` and `SECRET_KEY` are required. The app now fails fast at startup if either is missing.

### 3. Create tables

```bash
psql $DATABASE_URL -f schema.sql
```

Or copy the SQL into the Neon console.

### 4. Seed sample data

```bash
python seed.py
```

### 5. Run the app

```bash
python app.py
# → http://localhost:5000
```

### Production (gunicorn)

```bash
gunicorn "app:create_app()" -w 4 -b 0.0.0.0:8000
```

---

## Database Schema

| Table | Purpose |
|---|---|
| `authors` | Blog authors with bio & avatar |
| `categories` | Taxonomy (Mental Health, Neuroscience, etc.) |
| `articles` | Main content table (Markdown, featured flag, view count) |
| `tags` | Keyword tags |
| `article_tags` | Many-to-many junction |

---

## JSON API (for future CMS)

| Endpoint | Description |
|---|---|
| `GET /api/articles` | Paginated articles (`?page=`, `?category=`, `?q=`) |
| `GET /api/articles/<slug>` | Single article with tags & related |
| `GET /api/categories` | All categories with article counts |

---

## Adding Content

Insert a new article via SQL or psql:

```sql
INSERT INTO articles (title, slug, excerpt, content, cover_image_url, category_id, author_id, is_featured, reading_time_minutes, published_at)
VALUES (
  'My New Article',
  'my-new-article',
  'A short teaser...',
  '## Heading\n\nContent in **Markdown**.',
  'https://images.unsplash.com/photo-xxxx?w=1200',
  1,   -- category_id
  1,   -- author_id
  false,
  5,
  NOW()
);
```

Setting `published_at = NULL` keeps it as a draft.
