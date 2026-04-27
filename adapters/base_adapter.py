"""
BaseAdapter — the contract every database adapter must fulfil.

All methods return plain Python dicts / lists so the rest of the application
never touches SQL or ORM entities directly. Swapping the database is as simple as
implementing this interface in a new class.
"""

from abc import ABC, abstractmethod


class BaseAdapter(ABC):

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    @abstractmethod
    def connect(self) -> None:
        """Open / initialise the connection pool."""

    @abstractmethod
    def disconnect(self) -> None:
        """Close all connections gracefully."""

    # ── Articles ──────────────────────────────────────────────────────────────

    @abstractmethod
    def get_articles(
        self,
        page: int = 1,
        per_page: int = 9,
        category_slug: str | None = None,
        search_query: str | None = None,
    ) -> dict:
        """
        Return paginated articles.

        Returns
        -------
        {
            "items":      [article, ...],
            "total":      int,
            "page":       int,
            "per_page":   int,
            "pages":      int,
        }
        Each article dict contains: id, title, slug, excerpt, cover_image_url,
        published_at, category_name, category_slug, author_name, is_featured.
        """

    @abstractmethod
    def get_article_by_slug(self, slug: str) -> dict | None:
        """
        Return a single article with full content and related metadata,
        or None if not found.

        Extra fields versus get_articles: content, tags, related_articles.
        """

    @abstractmethod
    def get_featured_articles(self, limit: int = 3) -> list[dict]:
        """Return the most recently published featured articles."""

    @abstractmethod
    def get_recent_articles(self, limit: int = 6) -> list[dict]:
        """Return the most recently published articles (non-featured)."""

    # ── Categories ────────────────────────────────────────────────────────────

    @abstractmethod
    def get_categories(self) -> list[dict]:
        """
        Return all categories.

        Each dict: id, name, slug, description, article_count.
        """

    @abstractmethod
    def get_category_by_slug(self, slug: str) -> dict | None:
        """Return a single category or None."""

    # ── Tags ──────────────────────────────────────────────────────────────────

    @abstractmethod
    def get_tags(self) -> list[dict]:
        """Return all tags: id, name, slug, article_count."""

    # ── Trending / Sidebar ────────────────────────────────────────────────────

    @abstractmethod
    def get_trending_articles(self, limit: int = 5) -> list[dict]:
        """Return articles sorted by view_count desc (or published_at as fallback)."""

    # ── Stats (for future CMS) ────────────────────────────────────────────────

    @abstractmethod
    def increment_view_count(self, article_id: int) -> None:
        """Atomically increment the view counter for an article."""
