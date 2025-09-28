from flask import Flask, render_template, abort, url_for
from pathlib import Path
import frontmatter
from datetime import datetime
import re
from urllib.parse import quote

app = Flask(__name__)

def coerce_date(value, default_dt):
    """Convert various date formats to datetime object."""
    if isinstance(value, datetime):
        return value
    
    if isinstance(value, str):
        # Try various date formats
        for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%d/%m/%Y', '%m/%d/%Y']:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
    
    # Return None instead of file modification time
    return None

def extract_slug_from_filename(filename):
    """Extract slug from filename, removing date prefix if present."""
    name = filename.stem
    # Remove YYYY-MM-DD prefix if present
    date_prefix_pattern = r'^\d{4}-\d{2}-\d{2}-'
    return re.sub(date_prefix_pattern, '', name)

def load_posts():
    """Load all posts from the posts directory."""
    posts_dir = Path('posts')
    posts = []
    
    if not posts_dir.exists():
        return posts
    
    for md_file in posts_dir.glob('*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
            
            # Extract metadata
            meta = post.metadata
            slug = extract_slug_from_filename(md_file)
            
            # Handle date with proper fallback
            date = coerce_date(meta.get("date"), None)
            if date is None:
                # Try to extract date from filename
                filename = md_file.stem
                date_match = re.match(r'^(\d{4}-\d{2}-\d{2})', filename)
                if date_match:
                    try:
                        date = datetime.strptime(date_match.group(1), '%Y-%m-%d')
                    except ValueError:
                        pass
                
                # If still no date, use a fixed fallback date instead of file mtime
                if date is None:
                    print(f"WARNING: No valid date found for {slug}, using default date")
                    date = datetime(2024, 1, 1)  # Fixed fallback date
            
            # Build post data
            post_data = {
                'title': meta.get('title', slug.replace('-', ' ').title()),
                'date': date,
                'summary': meta.get('summary', ''),
                'tags': meta.get('tags', []),
                'cover': meta.get('cover', ''),
                'slug': slug,
                'content': post.content,
                'filename': md_file.name
            }
            
            posts.append(post_data)
            
        except Exception as e:
            print(f"Error loading post {md_file}: {e}")
            continue
    
    # Sort by date (newest first)
    posts.sort(key=lambda x: x['date'], reverse=True)
    return posts

def get_all_tags():
    """Get all unique tags from posts."""
    posts = load_posts()
    tags = set()
    for post in posts:
        tags.update(post['tags'])
    return sorted(tags)

@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts[:5])  # Show latest 5 posts

@app.route('/blog/')
def blog_index():
    posts = load_posts()
    return render_template('blog_index.html', posts=posts)

@app.route('/blog/<slug>/')
def blog_post(slug):
    posts = load_posts()
    post = next((p for p in posts if p['slug'] == slug), None)
    if not post:
        abort(404)
    return render_template('blog_post.html', post=post)

@app.route('/tags/')
def tags_index():
    tags = get_all_tags()
    posts = load_posts()
    
    # Group posts by tag
    tag_posts = {}
    for tag in tags:
        tag_posts[tag] = [p for p in posts if tag in p['tags']]
    
    return render_template('tags.html', tags=tags, tag_posts=tag_posts)

@app.route('/tags/<tag>/')
def tag_posts(tag):
    posts = load_posts()
    tagged_posts = [p for p in posts if tag in p['tags']]
    return render_template('tag_posts.html', tag=tag, posts=tagged_posts)

@app.route('/search/')
def search():
    return render_template('search.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/sitemap.xml')
def sitemap():
    """Generate XML sitemap for SEO."""
    posts = load_posts()
    
    # Static pages
    pages = [
        {'url': url_for('index', _external=True), 'lastmod': datetime.now().strftime('%Y-%m-%d')},
        {'url': url_for('blog_index', _external=True), 'lastmod': datetime.now().strftime('%Y-%m-%d')},
        {'url': url_for('tags_index', _external=True), 'lastmod': datetime.now().strftime('%Y-%m-%d')},
        {'url': url_for('about', _external=True), 'lastmod': datetime.now().strftime('%Y-%m-%d')},
        {'url': url_for('contact', _external=True), 'lastmod': datetime.now().strftime('%Y-%m-%d')},
    ]
    
    # Add blog posts
    for post in posts:
        pages.append({
            'url': url_for('blog_post', slug=post['slug'], _external=True),
            'lastmod': post['date'].strftime('%Y-%m-%d')
        })
    
    # Add tag pages
    tags = get_all_tags()
    for tag in tags:
        pages.append({
            'url': url_for('tag_posts', tag=tag, _external=True),
            'lastmod': datetime.now().strftime('%Y-%m-%d')
        })
    
    response = app.response_class(
        render_template('sitemap.xml', pages=pages),
        mimetype='application/xml'
    )
    return response

@app.route('/robots.txt')
def robots():
    """Generate robots.txt file."""
    response = app.response_class(
        render_template('robots.txt'),
        mimetype='text/plain'
    )
    return response

@app.route('/rss.xml')
def rss_feed():
    """Generate RSS feed."""
    posts = load_posts()[:10]  # Latest 10 posts
    
    response = app.response_class(
        render_template('rss.xml', posts=posts),
        mimetype='application/rss+xml'
    )
    return response

# Template filters
@app.template_filter('dateformat')
def dateformat(date, format='%B %d, %Y'):
    """Format date for templates."""
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')
    return date.strftime(format)

@app.template_filter('urlencode')
def urlencode_filter(s):
    """URL encode strings for templates."""
    return quote(str(s))

@app.template_filter('ymd')
def ymd_filter(date):
    """Format date as YYYY-MM-DD for templates."""
    if isinstance(date, str):
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return date
    return date.strftime('%Y-%m-%d')

# Template context processors
@app.context_processor
def inject_navigation():
    """Inject navigation data into all templates."""
    return {
        'nav_items': [
            {'name': 'Home', 'url': url_for('index')},
            {'name': 'Blog', 'url': url_for('blog_index')},
            {'name': 'Tags', 'url': url_for('tags_index')},
            {'name': 'About', 'url': url_for('about')},
            {'name': 'Contact', 'url': url_for('contact')},
        ]
    }

@app.template_global()
def now():
    """Make current datetime available to templates."""
    return datetime.now()

def build_tags():
    """Build tag pages for frozen site generation."""
    tags = get_all_tags()
    posts = load_posts()
    
    # Group posts by tag
    tag_posts = {}
    for tag in tags:
        tag_posts[tag] = [p for p in posts if tag in p['tags']]
    
    return tag_posts

if __name__ == '__main__':
    app.run(debug=True)