"""Blog routes — all public-facing pages."""

from flask import Blueprint, render_template, request, abort, g
from config import ARTICLES_PER_PAGE

blog_bp = Blueprint("blog", __name__)


def _sidebar_data() -> dict:
    """Shared sidebar data injected into every page."""
    db = g.db
    return {
        "sidebar_categories":  db.get_categories(),
        "sidebar_trending":    db.get_trending_articles(limit=4),
        "sidebar_tags":        db.get_tags(),
    }


# ── Home ──────────────────────────────────────────────────────────────────────

@blog_bp.route("/")
def index():
    db = g.db
    featured = db.get_featured_articles(limit=3)
    recent   = db.get_recent_articles(limit=6)
    return render_template(
        "index.html",
        featured=featured,
        recent=recent,
        **_sidebar_data(),
    )


# ── Blog listing ──────────────────────────────────────────────────────────────

@blog_bp.route("/blog")
def blog():
    db   = g.db
    page = request.args.get("page", 1, type=int)
    pagination = db.get_articles(page=page, per_page=ARTICLES_PER_PAGE)
    return render_template(
        "blog.html",
        pagination=pagination,
        current_category=None,
        **_sidebar_data(),
    )


# ── Single article ────────────────────────────────────────────────────────────

@blog_bp.route("/blog/<slug>")
def article(slug: str):
    db      = g.db
    post    = db.get_article_by_slug(slug)
    if post is None:
        abort(404)
    db.increment_view_count(post["id"])
    return render_template(
        "article.html",
        post=post,
        **_sidebar_data(),
    )


# ── Category ──────────────────────────────────────────────────────────────────

@blog_bp.route("/categories")
def categories():
    db   = g.db
    cats = db.get_categories()
    return render_template(
        "categories.html",
        categories=cats,
        **_sidebar_data(),
    )


@blog_bp.route("/categories/<slug>")
def category(slug: str):
    db  = g.db
    cat = db.get_category_by_slug(slug)
    if cat is None:
        abort(404)
    page = request.args.get("page", 1, type=int)
    pagination = db.get_articles(
        page=page,
        per_page=ARTICLES_PER_PAGE,
        category_slug=slug,
    )
    return render_template(
        "blog.html",
        pagination=pagination,
        current_category=cat,
        **_sidebar_data(),
    )


# ── Search ────────────────────────────────────────────────────────────────────

@blog_bp.route("/search")
def search():
    db    = g.db
    query = request.args.get("q", "").strip()
    page  = request.args.get("page", 1, type=int)
    pagination = db.get_articles(
        page=page,
        per_page=ARTICLES_PER_PAGE,
        search_query=query if query else None,
    ) if query else {"items": [], "total": 0, "pages": 0, "page": 1, "per_page": ARTICLES_PER_PAGE}
    return render_template(
        "search.html",
        pagination=pagination,
        query=query,
        **_sidebar_data(),
    )


# ── API endpoints (JSON — for future CMS) ────────────────────────────────────

from flask import jsonify

@blog_bp.route("/api/articles")
def api_articles():
    db   = g.db
    page = request.args.get("page", 1, type=int)
    cat  = request.args.get("category", None)
    q    = request.args.get("q", None)
    data = db.get_articles(page=page, per_page=ARTICLES_PER_PAGE,
                           category_slug=cat, search_query=q)
    # Convert datetime to string for JSON
    for item in data["items"]:
        if item.get("published_at"):
            item["published_at"] = str(item["published_at"])
    return jsonify(data)


@blog_bp.route("/api/articles/<slug>")
def api_article(slug: str):
    db   = g.db
    post = db.get_article_by_slug(slug)
    if post is None:
        return jsonify({"error": "Not found"}), 404
    if post.get("published_at"):
        post["published_at"] = str(post["published_at"])
    return jsonify(post)


@blog_bp.route("/api/categories")
def api_categories():
    return jsonify(g.db.get_categories())
