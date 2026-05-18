"""Repository layer around SQLAlchemy queries."""

from __future__ import annotations

from sqlalchemy import and_, func, or_, select, update
from sqlalchemy.orm import Session, joinedload

from adapters.orm_models import Article, Category, Tag, article_tags
from adapters.orm_models import User, ForumTopic, ForumPost


class UserRepository:
    def __init__(self, session: Session): self._session = session
    def by_id(self, user_id: int) -> User | None:
        return self._session.get(User, user_id)
    def by_username(self, username: str) -> User | None:
        return self._session.execute(select(User).where(User.username == username)).scalar_one_or_none()
    def create(self, **kwargs) -> User:
        user = User(**kwargs)
        self._session.add(user)
        return user

class ForumRepository:
    def __init__(self, session: Session): self._session = session
    def list_topics(self) -> list[ForumTopic]:
        return list(self._session.scalars(select(ForumTopic).order_by(ForumTopic.created_at.desc())).all())
    def topic_by_slug(self, slug: str) -> ForumTopic | None:
        return self._session.execute(select(ForumTopic).options(joinedload(ForumTopic.user), joinedload(ForumTopic.posts)).where(ForumTopic.slug == slug)).unique().scalars().first()
    def create_topic(self, **kwargs) -> ForumTopic:
        topic = ForumTopic(**kwargs)
        self._session.add(topic)
        return topic
    def create_post(self, **kwargs) -> ForumPost:
        post = ForumPost(**kwargs)
        self._session.add(post)
        return post


class ArticleRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def paginated(
        self,
        page: int,
        per_page: int,
        category_slug: str | None = None,
        search_query: str | None = None,
    ) -> dict:
        filters = [Article.published_at.is_not(None)]

        if category_slug:
            filters.append(Category.slug == category_slug)

        if search_query:
            q = f"%{search_query}%"
            filters.append(
                or_(
                    Article.title.ilike(q),
                    Article.excerpt.ilike(q),
                    Article.content.ilike(q),
                )
            )

        count_stmt = select(func.count(Article.id)).select_from(Article).outerjoin(Category)
        if filters:
            count_stmt = count_stmt.where(and_(*filters))

        total = int(self._session.execute(count_stmt).scalar_one() or 0)
        pages = max(1, (total + per_page - 1) // per_page)
        page = max(1, min(page, pages))
        offset = (page - 1) * per_page

        rows_stmt = (
            select(Article)
            .outerjoin(Category)
            .options(joinedload(Article.category), joinedload(Article.author))
            .where(and_(*filters))
            .order_by(Article.published_at.desc())
            .limit(per_page)
            .offset(offset)
        )

        items = list(self._session.scalars(rows_stmt).all())
        return {
            "items": items,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": pages,
        }

    def by_slug(self, slug: str) -> Article | None:
        stmt = (
            select(Article)
            .options(
                joinedload(Article.category),
                joinedload(Article.author),
                joinedload(Article.tags),
            )
            .where(Article.slug == slug)
        )
        return self._session.execute(stmt).unique().scalars().first()

    def related(self, category_slug: str | None, exclude_slug: str, limit: int = 3) -> list[Article]:
        if not category_slug:
            return []

        stmt = (
            select(Article)
            .join(Category)
            .options(joinedload(Article.category), joinedload(Article.author))
            .where(
                Category.slug == category_slug,
                Article.slug != exclude_slug,
                Article.published_at.is_not(None),
            )
            .order_by(Article.published_at.desc())
            .limit(limit)
        )
        return list(self._session.scalars(stmt).all())

    def featured(self, limit: int) -> list[Article]:
        stmt = (
            select(Article)
            .options(joinedload(Article.category), joinedload(Article.author))
            .where(Article.is_featured.is_(True), Article.published_at.is_not(None))
            .order_by(Article.published_at.desc())
            .limit(limit)
        )
        return list(self._session.scalars(stmt).all())

    def recent(self, limit: int) -> list[Article]:
        stmt = (
            select(Article)
            .options(joinedload(Article.category), joinedload(Article.author))
            .where(Article.published_at.is_not(None))
            .order_by(Article.published_at.desc())
            .limit(limit)
        )
        return list(self._session.scalars(stmt).all())

    def trending(self, limit: int) -> list[Article]:
        stmt = (
            select(Article)
            .options(joinedload(Article.category), joinedload(Article.author))
            .where(Article.published_at.is_not(None))
            .order_by(Article.view_count.desc(), Article.published_at.desc())
            .limit(limit)
        )
        return list(self._session.scalars(stmt).all())

    def increment_view_count(self, article_id: int) -> None:
        stmt = update(Article).where(Article.id == article_id).values(view_count=Article.view_count + 1)
        self._session.execute(stmt)


class TaxonomyRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def categories(self) -> list[dict]:
        stmt = (
            select(
                Category.id,
                Category.name,
                Category.slug,
                Category.description,
                func.count(Article.id).label("article_count"),
            )
            .outerjoin(Article, and_(Article.category_id == Category.id, Article.published_at.is_not(None)))
            .group_by(Category.id)
            .order_by(Category.name)
        )
        return [
            {
                "id": row.id,
                "name": row.name,
                "slug": row.slug,
                "description": row.description,
                "article_count": int(row.article_count or 0),
            }
            for row in self._session.execute(stmt)
        ]

    def category_by_slug(self, slug: str) -> dict | None:
        stmt = (
            select(
                Category.id,
                Category.name,
                Category.slug,
                Category.description,
                func.count(Article.id).label("article_count"),
            )
            .outerjoin(Article, and_(Article.category_id == Category.id, Article.published_at.is_not(None)))
            .where(Category.slug == slug)
            .group_by(Category.id)
        )
        row = self._session.execute(stmt).first()
        if not row:
            return None
        return {
            "id": row.id,
            "name": row.name,
            "slug": row.slug,
            "description": row.description,
            "article_count": int(row.article_count or 0),
        }

    def tags(self) -> list[dict]:
        stmt = (
            select(
                Tag.id,
                Tag.name,
                Tag.slug,
                func.count(article_tags.c.article_id).label("article_count"),
            )
            .outerjoin(article_tags, Tag.id == article_tags.c.tag_id)
            .group_by(Tag.id)
            .order_by(func.count(article_tags.c.article_id).desc())
        )
        return [
            {
                "id": row.id,
                "name": row.name,
                "slug": row.slug,
                "article_count": int(row.article_count or 0),
            }
            for row in self._session.execute(stmt)
        ]
