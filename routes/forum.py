from flask import Blueprint, render_template, request, redirect, url_for, g
from flask_login import login_required, current_user
import slugify

forum_bp = Blueprint('forum', __name__)

@forum_bp.route('/forum')
@login_required
def index():
    topics = g.db.get_all_topics()
    return render_template('forum/index.html', topics=topics)

@forum_bp.route('/forum/new', methods=['GET', 'POST'])
@login_required
def create_topic():
    article_id = request.args.get('article_id')
    article = None
    if article_id:
        article = g.db.get_article_by_id(int(article_id))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        slug = slugify.slugify(title)
        
        g.db.create_topic(
            title=title, 
            content=content, 
            slug=slug, 
            user_id=current_user.id,
            article_id=article_id if article_id else None
        )
        return redirect(url_for('forum.index'))
    
    return render_template('forum/create_topic.html', article=article)

@forum_bp.route('/forum/t/<slug>', methods=['GET', 'POST'])
@login_required
def view_topic(slug):
    topic = g.db.get_topic_by_slug(slug)
    
    if request.method == 'POST':
        content = request.form.get('content')
        # ── Capture the parent_id from the reply form ──
        parent_id = request.form.get('parent_id') 
        
        g.db.create_post(
            content=content, 
            topic_id=topic.id, 
            user_id=current_user.id,
            # Convert to int if it exists, otherwise pass None
            parent_id=int(parent_id) if parent_id else None
        )
        return redirect(url_for('forum.view_topic', slug=slug))
    
    # ── Filter: Get only top-level posts (those without a parent) ──
    # The template will use the 'replies' relationship to render the tree recursively.
    root_posts = [p for p in topic.posts if p.parent_id is None]
    
    return render_template('forum/topic.html', topic=topic, root_posts=root_posts)