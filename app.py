"""
Healthy dwelling — Flask Application
"""

import markdown as md_lib
from flask import Flask, g
from config import SECRET_KEY, DEBUG, APP_HOST, APP_PORT
from adapters import get_adapter
from routes.blog import blog_bp
from flask_login import LoginManager
from routes.auth import auth_bp
from routes.forum import forum_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    # ── Jinja globals & filters ───────────────────────────────────────────────
    @app.template_filter("markdown")
    def markdown_filter(text: str) -> str:
        if not text:
            return ""
        return md_lib.markdown(
            text,
            extensions=["extra", "codehilite", "toc"],
        )

    @app.template_filter("dateformat")
    def dateformat_filter(value, fmt="%B %d, %Y"):
        if value is None:
            return ""
        if hasattr(value, "strftime"):
            return value.strftime(fmt)
        return str(value)

    # ── Adapter lifecycle ─────────────────────────────────────────────────────
    @app.before_request
    def open_db():
        g.db = get_adapter()
        g.db.connect()

    @app.teardown_appcontext
    def close_db(exc):
        db = g.pop("db", None)
        if db is not None:
            db.disconnect()

    # ── Blueprints ────────────────────────────────────────────────────────────
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        adapter = get_adapter()
        adapter.connect()
        return adapter.get_user_by_id(int(user_id))
    
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(forum_bp)
    app.register_blueprint(blog_bp)
    

    return app


app = create_app()

if __name__ == "__main__":
    # This only runs when you execute 'python app.py' locally
    app.run(debug=DEBUG, host=APP_HOST, port=APP_PORT)
