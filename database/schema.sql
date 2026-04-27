-- ============================================================
--  Minds & Mysteries — PostgreSQL Schema
--  Run this once against your Neon database:
--    psql $DATABASE_URL -f schema.sql
-- ============================================================

-- ── Authors ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS authors (
    id           SERIAL PRIMARY KEY,
    name         VARCHAR(200) NOT NULL,
    bio          TEXT,
    avatar_url   TEXT,
    website_url  TEXT,
    created_at   TIMESTAMPTZ DEFAULT NOW()
);

-- ── Categories ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS categories (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    slug        VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ── Articles ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS articles (
    id                     SERIAL PRIMARY KEY,
    title                  VARCHAR(500) NOT NULL,
    slug                   VARCHAR(500) UNIQUE NOT NULL,
    excerpt                TEXT,
    content                TEXT,           -- Markdown
    cover_image_url        TEXT,
    category_id            INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    author_id              INTEGER REFERENCES authors(id)    ON DELETE SET NULL,
    is_featured            BOOLEAN DEFAULT FALSE,
    view_count             INTEGER DEFAULT 0,
    reading_time_minutes   INTEGER DEFAULT 5,
    meta_title             VARCHAR(500),
    meta_description       TEXT,
    published_at           TIMESTAMPTZ,    -- NULL = draft
    created_at             TIMESTAMPTZ DEFAULT NOW(),
    updated_at             TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_articles_slug         ON articles(slug);
CREATE INDEX IF NOT EXISTS idx_articles_category     ON articles(category_id);
CREATE INDEX IF NOT EXISTS idx_articles_published    ON articles(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_articles_featured     ON articles(is_featured) WHERE is_featured = TRUE;

-- ── Tags ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS tags (
    id    SERIAL PRIMARY KEY,
    name  VARCHAR(100) NOT NULL,
    slug  VARCHAR(100) UNIQUE NOT NULL
);

-- ── Article ↔ Tags (junction) ─────────────────────────────────
CREATE TABLE IF NOT EXISTS article_tags (
    article_id  INTEGER NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    tag_id      INTEGER NOT NULL REFERENCES tags(id)     ON DELETE CASCADE,
    PRIMARY KEY (article_id, tag_id)
);

-- ── auto-update updated_at ───────────────────────────────────
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_articles_updated_at ON articles;
CREATE TRIGGER trg_articles_updated_at
    BEFORE UPDATE ON articles
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
