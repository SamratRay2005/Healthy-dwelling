"""Unit of Work for request-scoped SQLAlchemy sessions."""

from __future__ import annotations

from sqlalchemy.orm import Session, sessionmaker
from adapters.repositories import ArticleRepository, TaxonomyRepository, UserRepository, ForumRepository


class SqlAlchemyUnitOfWork:
    """Owns one SQLAlchemy session and exposes repositories."""

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory
        self.session: Session | None = None

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        self.session = self._session_factory()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if not self.session:
            return
        if exc_type:
            self.session.rollback()
        self.session.close()
        self.session = None

    def commit(self) -> None:
        if self.session is None:
            raise RuntimeError("UnitOfWork session not started")
        self.session.commit()

    @property
    def users(self) -> UserRepository:
        if self.session is None: raise RuntimeError("Session not started")
        return UserRepository(self.session)

    @property
    def forum(self) -> ForumRepository:
        if self.session is None: raise RuntimeError("Session not started")
        return ForumRepository(self.session)

    @property
    def articles(self) -> ArticleRepository:
        if self.session is None:
            raise RuntimeError("UnitOfWork session not started")
        return ArticleRepository(self.session)

    @property
    def taxonomy(self) -> TaxonomyRepository:
        if self.session is None:
            raise RuntimeError("UnitOfWork session not started")
        return TaxonomyRepository(self.session)
