"""PostgreSQL adapter implemented with SQLAlchemy ORM and repositories."""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from adapters.base_adapter import BaseAdapter
from adapters.orm_models import Article
from adapters.unit_of_work import SqlAlchemyUnitOfWork


class PostgreSQLAdapter(BaseAdapter):
    """Adapter + Repository + Unit of Work composition.

    Public methods keep returning plain dict/list payloads so route/template
    code stays decoupled from ORM entities.
    """

    def __init__(self, database_url: str) -> None:
        self._engine = create_engine(database_url, pool_pre_ping=True, future=True)
        self._session_factory = sessionmaker(bind=self._engine, autoflush=False, expire_on_commit=False)
        self._uow: SqlAlchemyUnitOfWork | None = None

    def connect(self) -> None:
        if self._uow is None:
            self._uow = SqlAlchemyUnitOfWork(self._session_factory)
            self._uow.__enter__()

    def disconnect(self) -> None:
        if self._uow is not None:
            self._uow.__exit__(None, None, None)
            self._uow = None

    def _require_uow(self) -> SqlAlchemyUnitOfWork:
        if self._uow is None:
            self.connect()
        if self._uow is None:
            raise RuntimeError("Database unit of work not available")
        return self._uow

    @staticmethod
    def _article_to_dict(article: Article) -> dict:
        return {
            "id": article.id,
            "title": article.title,
            "slug": article.slug,
            "excerpt": article.excerpt,
            "cover_image_url": article.cover_image_url,
            "is_featured": article.is_featured,
            "view_count": article.view_count,
            "published_at": article.published_at,
            "reading_time_minutes": article.reading_time_minutes,
            "category_name": article.category.name if article.category else None,
            "category_slug": article.category.slug if article.category else None,
            "author_name": article.author.name if article.author else None,
            "author_avatar": article.author.avatar_url if article.author else None,
        }

    def get_articles(
        self,
        page: int = 1,
        per_page: int = 9,
        category_slug: str | None = None,
        search_query: str | None = None,
    ) -> dict:
        uow = self._require_uow()
        data = uow.articles.paginated(
            page=page,
            per_page=per_page,
            category_slug=category_slug,
            search_query=search_query,
        )
        data["items"] = [self._article_to_dict(article) for article in data["items"]]
        return data

    def get_article_by_slug(self, slug: str) -> dict | None:
        uow = self._require_uow()
        article = uow.articles.by_slug(slug)
        if article is None:
            return None

        payload = self._article_to_dict(article)
        payload["content"] = article.content
        payload["meta_title"] = article.meta_title
        payload["meta_description"] = article.meta_description
        payload["tags"] = [{"name": tag.name, "slug": tag.slug} for tag in article.tags]

        related = uow.articles.related(payload["category_slug"], slug, limit=3)
        payload["related_articles"] = [self._article_to_dict(item) for item in related]
        return payload

    def get_featured_articles(self, limit: int = 3) -> list[dict]:
        uow = self._require_uow()
        return [self._article_to_dict(item) for item in uow.articles.featured(limit)]

    def get_recent_articles(self, limit: int = 6) -> list[dict]:
        uow = self._require_uow()
        return [self._article_to_dict(item) for item in uow.articles.recent(limit)]

    def get_categories(self) -> list[dict]:
        uow = self._require_uow()
        return uow.taxonomy.categories()

    def get_category_by_slug(self, slug: str) -> dict | None:
        uow = self._require_uow()
        return uow.taxonomy.category_by_slug(slug)

    def get_tags(self) -> list[dict]:
        uow = self._require_uow()
        return uow.taxonomy.tags()

    def get_trending_articles(self, limit: int = 5) -> list[dict]:
        uow = self._require_uow()
        return [self._article_to_dict(item) for item in uow.articles.trending(limit)]

    def increment_view_count(self, article_id: int) -> None:
        uow = self._require_uow()
        uow.articles.increment_view_count(article_id)
        uow.commit()
