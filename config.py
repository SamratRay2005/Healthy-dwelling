import os
from dotenv import load_dotenv

load_dotenv()


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

# ─── Database ─────────────────────────────────────────────────────────────────
DATABASE_URL = _require_env("DATABASE_URL")

# ─── Adapter Selection ─────────────────────────────────────────────────────────
# Swap this to 'mock' or 'mysql' etc. to change the database backend.
DB_ADAPTER = os.environ.get("DB_ADAPTER", "postgres")

# ─── Flask ────────────────────────────────────────────────────────────────────
SECRET_KEY = _require_env("SECRET_KEY")
DEBUG = os.environ.get("DEBUG", "False").strip().lower() in {"1", "true", "yes", "on"}
APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT = int(os.environ.get("APP_PORT", "5001"))

# ─── Pagination ───────────────────────────────────────────────────────────────
ARTICLES_PER_PAGE = int(os.environ.get("ARTICLES_PER_PAGE", 9))
