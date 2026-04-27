"""
Adapter package — import get_adapter() to obtain the active database adapter.

To add a new backend:
  1. Create adapters/my_backend_adapter.py implementing BaseAdapter
  2. Register it in the ADAPTER_REGISTRY dict below
  3. Set DB_ADAPTER=my_backend in .env or the environment
"""

from config import DB_ADAPTER, DATABASE_URL
from adapters.base_adapter import BaseAdapter
from adapters.postgres_adapter import PostgreSQLAdapter

# ── Registry ──────────────────────────────────────────────────────────────────
ADAPTER_REGISTRY: dict[str, type[BaseAdapter]] = {
    "postgres": PostgreSQLAdapter,
    # "mysql":   MySQLAdapter,      # add future adapters here
    # "mock":    MockAdapter,
}


def get_adapter() -> BaseAdapter:
    """Return a fully-constructed adapter instance based on DB_ADAPTER env var."""
    cls = ADAPTER_REGISTRY.get(DB_ADAPTER)
    if cls is None:
        raise ValueError(
            f"Unknown DB_ADAPTER '{DB_ADAPTER}'. "
            f"Valid options: {list(ADAPTER_REGISTRY.keys())}"
        )
    return cls(DATABASE_URL)
