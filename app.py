from flask import Flask, render_template, abort, url_for, redirect, request
from pathlib import Path
import frontmatter
from datetime import datetime
import re
from urllib.parse import quote, unquote
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from hubs_config import get_hub_config, get_all_hubs, get_hub_navigation
from config.tag_descriptions import get_tag_description
import json

app = Flask(__name__)

# Site configuration
app.config['SITE_NAME'] = 'Azure Noob'
app.config['SITE_TAGLINE'] = "Don't be a Noob"
app.config['SITE_URL'] = 'https://azure-noob.com'

# Quiet missing-date warnings + accept more formats
WARNED_SLUGS = set()

# ===== FIX 404 ERRORS AND CANONICAL URL ISSUES =====
@app.before_request
def handle_trailing_slashes_and_redirects():
    """
    Single-pass redirect handler to eliminate redirect chains.
    Checks ALL conditions once and builds final URL, then redirects once (or not at all).
    
    This fixes Google Search Console "Page with redirect" errors by ensuring
    no more than ONE 301 redirect per request.
    """
    # Track original request details
    original_scheme = request.scheme
    original_host = request.host
    original_path = request.path
    
    # Initialize final URL components (start with originals)
    final_scheme = original_scheme
    final_host = original_host
    final_path = original_path
    needs_redirect = False
    
    # 1. Force HTTPS
    if final_scheme == 'http':
        final_scheme = 'https'
        needs_redirect = True
    
    # 2. Force non-WWW
    if final_host.startswith('www.'):
        final_host = final_host.replace('www.', '', 1)
        needs_redirect = True
    
    # 3. Root path - no changes needed
    if final_path == '/':
        if needs_redirect:
            return redirect(f'{final_scheme}://{final_host}{final_path}', code=301)
        return None
    
    # 4. File-like endpoints - no trailing slash changes
    if any(final_path.endswith(ext) for ext in ['.xml', '.json', '.txt', '.rss', '.atom']):
        if needs_redirect:
            return redirect(f'{final_scheme}://{final_host}{final_path}', code=301)
        return None
    
    # 5. Strategic redirects (high-priority money pages)
    strategic_redirects = {
        '/azure-openai-pricing/': '/blog/azure-openai-pricing-real-costs/',
        '/azure-openai-pricing-2026/': '/blog/azure-openai-pricing-real-costs/',
        '/azure-openai-cost/': '/blog/azure-openai-pricing-real-costs/',
        '/azure-finops/': '/blog/azure-finops-complete-guide/',
        '/finops-azure/': '/blog/azure-finops-complete-guide/',
        '/kql-cheat-sheet/': '/blog/kql-cheat-sheet-complete/',
        '/kql-query-library/': '/products/',
    }
    
    if final_path in strategic_redirects:
        final_path = strategic_redirects[final_path]
        needs_redirect = True
    
    # 6. Remove /index.html suffix
    if final_path.endswith('/index.html'):
        final_path = final_path.replace('/index.html', '/')
        needs_redirect = True
    
    # 7. Remove date prefix from blog URLs
    # Example: /blog/2025-01-15-kql-cheat-sheet-complete/ -> /blog/kql-cheat-sheet-complete/
    if '/blog/' in final_path and re.match(r'.*/blog/\d{4}-\d{2}-\d{2}-.+', final_path):
        parts = final_path.split('/')
        for i, part in enumerate(parts):
            if re.match(r'^\d{4}-\d{2}-\d{2}-.+', part):
                parts[i] = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', part)
                final_path = '/'.join(parts)
                needs_redirect = True
                break
    
    # 8. Slugify tag URLs
    if '/tags/' in final_path:
        tag_match = re.match(r'/tags/([^/]+)/?$', final_path)
        if tag_match:
            tag_from_url = tag_match.group(1)
            tag_slugified = slugify_tag(unquote(tag_from_url))
            if tag_from_url != tag_slugified:
                final_path = f'/tags/{tag_slugified}/'
                needs_redirect = True
    
    # 9. Add trailing slash if missing
    if not final_path.endswith('/'):
        final_path += '/'
        needs_redirect = True
    
    # Perform single redirect if any changes were needed
    if needs_redirect:
        final_url = f'{final_scheme}://{final_host}{final_path}'
        return redirect(final_url, code=301)
    
    return None

def get_canonical_url():
    """Generate canonical URL for current request with trailing slash."""
    site_url = app.config.get('SITE_URL', 'https://azure-noob.com')
    path = request.path if request.path.endswith('/') else request.path + '/'
    return f"{site_url}{path}"

def coerce_date(value, default_dt):
    """Convert various date formats to datetime object."""
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        for fmt in [
            '%Y-%m-%d', '%Y/%m/%d', '%d/%m/%Y', '%m/%d/%Y',
            '%Y-%m-%dT%H:%M:%SZ',   # e.g., 2025-10-02T14:20:00Z
            '%Y-%m-%dT%H:%M:%S',    # e.g., 2025-10-02T14:20:00
        ]:
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

def fix_internal_links(html_content):
    """
    Post-process rendered HTML to fix internal link issues:
    1. Ensure trailing slashes on internal /blog/, /tags/, /hub/ links
    2. Strip date prefixes from any /blog/YYYY-MM-DD-slug links
    """
    import re as _re
    
    def fix_link(match):
        prefix = match.group(1)  # 'href="'
        path = match.group(2)    # the URL path
        suffix = match.group(3)  # '"' closing quote
        
        # Strip date prefix from blog links: /blog/2025-01-15-slug -> /blog/slug
        path = _re.sub(r'^(/blog/)(\d{4}-\d{2}-\d{2}-)', r'\1', path)
        
        # Add trailing slash if missing (skip anchors and file extensions)
        if not path.endswith('/') and '#' not in path and not _re.search(r'\.[a-zA-Z0-9]+$', path):
            path += '/'
        
        return f'{prefix}{path}{suffix}'
    
    # Match href attributes pointing to internal paths
    html_content = _re.sub(
        r'(href=")(/(?:blog|tags|hub|hubs|about|search|start-here|products)/[^"]*)(")',
        fix_link,
        html_content
    )
    
    return html_content


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

                # If still no date, use a fixed fallback date (quietly)
                if date is None:
                    if slug not in WARNED_SLUGS:
                        app.logger.debug(f"No valid date found for '{slug}', defaulting to 2024-01-01")
                        WARNED_SLUGS.add(slug)
                    date = datetime(2024, 1, 1)  # Fixed fallback date

            # Build post data
            cover = meta.get('cover', '')
            # Normalize cover path: remove leading slash if present
            if cover and cover.startswith('/'):
                cover = cover[1:]  # Remove leading slash
            
            post_data = {
                'title': meta.get('title', slug.replace('-', ' ').title()),
                'date': date,
                'modified': meta.get('modified', date),  # Track modified date
                'summary': meta.get('summary', ''),
                'tags': meta.get('tags', []),
                'cover': cover,
                'cover_url': f"/{cover}" if cover else '',  # Always use absolute path for templates
                'slug': slug,
                'content': post.content,
                'filename': md_file.name,
                'faq_schema': meta.get('faq_schema', False),  # Add FAQ schema flag
                'proficiency_level': meta.get('proficiency_level', 'Intermediate'),
                'dependencies': meta.get('dependencies', ''),
                'is_howto': meta.get('is_howto', False),
            }

            posts.append(post_data)

        except Exception as e:
            # Keep this error to help diagnose malformed frontmatter or encoding issues
            app.logger.error(f"Error loading post {md_file}: {e}")
            continue

    # Sort by date (newest first)
    posts.sort(key=lambda x: x['date'], reverse=True)
    return posts

def get_all_tags():
    """Get all unique tags from posts."""
    posts = load_posts()
    tags = set()
    for post in posts:
        # Slugify tags to ensure URL-safe versions
        tags.update([slugify_tag(tag) for tag in post['tags']])
    return sorted(tags)

def get_related_posts(current_post, limit=3):
    """Get related posts based on shared tags."""
    all_posts = load_posts()

    # Remove current post from candidates
    candidates = [p for p in all_posts if p['slug'] != current_post['slug']]

    # Score each post by number of shared tags
    scored_posts = []
    current_tags = set(current_post['tags'])

    for post in candidates:
        post_tags = set(post['tags'])
        shared_tags = current_tags.intersection(post_tags)
        if shared_tags:
            scored_posts.append((len(shared_tags), post))

    # Sort by score (descending), then by date (newest first)
    scored_posts.sort(key=lambda x: (x[0], x[1]['date']), reverse=True)

    # Return top N posts
    return [post for score, post in scored_posts[:limit]]

def generate_meta_description(summary, content, max_length=160):
    """
    Generate optimal meta description from summary or content.
    SEO best practice: 150-160 characters
    """
    if summary and len(summary) <= max_length:
        return summary
    
    if summary:
        # Truncate summary intelligently at word boundary
        truncated = summary[:max_length - 3]
        last_space = truncated.rfind(' ')
        if last_space > 0:
            truncated = truncated[:last_space]
        return truncated + '...'
    
    # Extract from content if no summary
    text_only = re.sub('<[^<]+?>', '', content)  # Strip HTML
    text_only = ' '.join(text_only.split())  # Normalize whitespace
    
    if len(text_only) <= max_length:
        return text_only
    
    truncated = text_only[:max_length - 3]
    last_space = truncated.rfind(' ')
    if last_space > 0:
        truncated = truncated[:last_space]
    return truncated + '...'


def slugify_tag(tag):
    """
    Convert tag names to URL-safe slugs.
    Examples:
        'Hybrid Cloud' -> 'hybrid-cloud'
        'DNS Resolver' -> 'dns-resolver'
        'Azure' -> 'azure'
    """
    return tag.lower().replace(' ', '-').replace(',', '').strip()


def load_faq_schema(slug):
    """
    Load FAQ schema JSON for a post if it exists.
    Returns script tag with JSON-LD for injection into template.
    """
    schema_path = Path('schema') / f'{slug}-faq-schema.json'
    if schema_path.exists():
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_data = json.load(f)
            # Wrap in script tag for injection
            return f'<script type="application/ld+json">\n{json.dumps(schema_data, indent=2)}\n</script>'
        except Exception as e:
            app.logger.error(f"Error loading FAQ schema for {slug}: {e}")
            return None
    return None



@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', 
                         posts=posts[:5],
                         canonical_url=get_canonical_url(),
                         page_title='Azure Noob - Azure Cloud Tutorials & Guides',
                         meta_description='Learn Azure from a fellow noob. Practical tutorials, real-world scenarios, and honest takes on Azure cloud architecture.')

@app.route('/blog/')
def blog_index():
    posts = load_posts()
    return render_template('blog_index.html', 
                         posts=posts,
                         canonical_url=get_canonical_url(),
                         page_title='70+ Azure Production Battle Stories: Real Enterprise Problems Microsoft Won\'t Document',
                         meta_description='114+ Azure guides from managing 31,000+ resources across 44 subscriptions: Cost allocation templates, KQL queries for inventory, governance policies teams follow, Arc ghost cleanup scripts, OpenAI pricing breakdowns. Production-tested solutions updated 2x/week.')

@app.route('/blog/<slug>/')
def blog_post(slug):
    posts = load_posts()
    post = next((p for p in posts if p['slug'] == slug), None)
    if not post:
        abort(404)

    # Find current post index for prev/next navigation
    current_index = next((i for i, p in enumerate(posts) if p['slug'] == slug), None)
    prev_post = posts[current_index + 1] if current_index is not None and current_index + 1 < len(posts) else None
    next_post = posts[current_index - 1] if current_index is not None and current_index > 0 else None

    # Process markdown with syntax highlighting
    content = markdown.markdown(
        post['content'],
        extensions=[
            CodeHiliteExtension(linenums=False, css_class='codehilite'),
            FencedCodeExtension(),
            'tables',
            'nl2br',
            'toc',
        ],
        extension_configs={
            'toc': {
                'permalink': False,
                'slugify': lambda value, separator: re.sub(r'[^\w]+', separator, value.lower()).strip(separator),
            }
        }
    )

    # Fix internal links (trailing slashes + date prefix removal)
    content = fix_internal_links(content)

    cover_url = post['cover'] if post['cover'] else None

    # Calculate reading time (rough estimate: 200 words per minute)
    word_count = len(content.split())
    reading_min = max(1, round(word_count / 200))

    # Get related posts
    related = get_related_posts(post, limit=3)


    # ===== SEO ENHANCEMENTS =====
    
    # Auto-generate optimal meta description
    meta_description = generate_meta_description(
        post.get('summary', ''),
        content,
        max_length=160
    )
    
    # Build full OG image URL
    site_url = app.config.get('SITE_URL', 'https://azure-noob.com')
    if cover_url:
        # Ensure proper URL construction
        cover_clean = cover_url.lstrip('/')
        og_image = f"{site_url}/{cover_clean}"
    else:
        og_image = f"{site_url}/static/images/hero/cloud-wars.png"
    
    # Build canonical URL
    canonical_url = f"{site_url}{url_for('blog_post', slug=slug)}"
    
    # ISO date formats for Open Graph and JSON-LD
    date_published_iso = post['date'].strftime('%Y-%m-%dT%H:%M:%S+00:00')
    
    # Use modified date if available, otherwise use published date
    modified_date = post.get('modified', post['date'])
    if isinstance(modified_date, str):
        modified_date = coerce_date(modified_date, post['date'])
    date_modified_iso = modified_date.strftime('%Y-%m-%dT%H:%M:%S+00:00')


    return render_template('blog_post.html',
                           post=post,
                           content=content,
                           cover_url=cover_url,
                           reading_min=reading_min,
                           prev_post=prev_post,
                           next_post=next_post,
                           related_posts=related,
                           word_count=word_count,
                           # SEO variables for base.html
                           page_title=post['title'],
                           meta_description=meta_description,
                           canonical_url=canonical_url,
                           og_type='article',
                           og_image=og_image,
                           og_tags=post.get('tags', []),
                           date_published_iso=date_published_iso,
                           date_modified_iso=date_modified_iso,
                           author_name='David Swann',
                           faq_schema_json=load_faq_schema(slug))

@app.route('/tags/')
def tags_index():
    all_tags = get_all_tags()  # Returns slugified tags
    posts = load_posts()

    # Group posts by tag and create (tag_slug, count) tuples
    tag_posts = {}
    tags_with_counts = []

    print(f"\n=== TAGS_INDEX ROUTE DEBUG ===")
    print(f"Total slugified tags: {len(all_tags)}")
    
    for tag_slug in all_tags:
        # Match posts by slugified tag comparison
        tag_posts[tag_slug] = [p for p in posts if any(slugify_tag(t) == tag_slug for t in p['tags'])]
        tags_with_counts.append((tag_slug, len(tag_posts[tag_slug])))
    
    # Check what we're passing
    problem_tags = ['Active Directory', 'active-directory', 'Azure AD', 'azure-ad']
    for pt in problem_tags:
        found = any(t == pt for t, c in tags_with_counts)
        if found:
            print(f"  WARNING: Passing '{pt}' to template")
    
    print(f"First 10 tags being passed: {[t for t, c in tags_with_counts[:10]]}")
    print("=== END TAGS_INDEX DEBUG ===\n")

    return render_template('tags_index.html', 
                         tags=tags_with_counts, 
                         tag_posts=tag_posts,
                         canonical_url=get_canonical_url(),
                         page_title='Tags - Azure Noob',
                         meta_description='Browse Azure tutorials by tag.')

@app.route('/tags/<tag>/')
def tag_posts(tag):
    posts = load_posts()
    # Match posts by slugified tag
    tag_slug = slugify_tag(tag)
    tagged_posts = [p for p in posts if any(slugify_tag(t) == tag_slug for t in p['tags'])]
    
    # Find original tag name (with proper casing) for display
    original_tag = tag
    for post in tagged_posts:
        for t in post['tags']:
            if slugify_tag(t) == tag_slug:
                original_tag = t
                break
    
    # Get tag description data for SEO
    tag_data = get_tag_description(tag_slug)
    
    site_url = app.config.get('SITE_URL', 'https://azure-noob.com')
    canonical_url = f"{site_url}/tags/{tag_slug}/"
    
    # Generate meta description from tag data or fall back to default
    if tag_data and tag_data.get('description'):
        # Use first 160 characters of description for meta
        desc_text = tag_data['description'][:160].strip()
        # Find last complete sentence
        last_period = desc_text.rfind('.')
        if last_period > 100:
            desc_text = desc_text[:last_period + 1]
        meta_description = desc_text
    else:
        meta_description = f'Azure tutorials and guides about {original_tag}.'
    
    return render_template('tags.html', 
                         tag=original_tag,  # Display name
                         tag_slug=tag_slug,  # URL slug
                         tag_data=tag_data,  # Description and CTA data
                         posts=tagged_posts,
                         canonical_url=canonical_url,
                         page_title=f'{original_tag} - Azure Noob',
                         meta_description=meta_description)

@app.route('/search/')
def search():
    return render_template('search.html',
                         canonical_url=get_canonical_url(),
                         page_title='Search - Azure Noob',
                         meta_description='Search Azure Noob tutorials and guides.')

@app.route('/search.json')
def search_json():
    """Return all posts as JSON for client-side search."""
    posts = load_posts()
    # Return simplified post data for search
    search_data = []
    for post in posts:
        search_data.append({
            'title': post['title'],
            'summary': post['summary'],
            'slug': post['slug'],
            'date': post['date'].strftime('%Y-%m-%d'),
            'tags': post['tags'],
            'url': url_for('blog_post', slug=post['slug'])
        })

    from flask import jsonify
    response = jsonify(search_data)
    # Add noindex header to prevent Google indexing this API endpoint
    response.headers['X-Robots-Tag'] = 'noindex'
    return response

@app.route('/about/')
def about():
    return render_template('about.html',
                         canonical_url=get_canonical_url(),
                         page_title='About - Azure Noob',
                         meta_description='About Azure Noob and David Swann.')

@app.route('/start-here/')
def start_here():
    return render_template('start_here.html',
                         canonical_url=get_canonical_url(),
                         page_title='Start Here - Azure Noob',
                         meta_description='New to Azure Noob? Start here for the best Azure tutorials.')

@app.route('/products/')
def products():
    return render_template('products.html',
                         canonical_url=get_canonical_url(),
                         page_title='Digital Products for Azure Admins | Azure Noob',
                         meta_description='Production-tested Azure tools and guides. KQL Query Library, Admin Reference Library, and more from managing 30,000+ resources.')

@app.route('/hubs/')
def hubs_index():
    """List all content hubs."""
    hubs = get_all_hubs()
    return render_template('hubs_index.html', 
                         hubs=hubs,
                         canonical_url=get_canonical_url(),
                         page_title='Content Hubs - Azure Noob',
                         meta_description='Curated Azure learning paths and content hubs.')

@app.route('/hub/<slug>/')
def hub_page(slug):
    """Display a specific content hub."""
    hub_config = get_hub_config(slug)
    if not hub_config:
        abort(404)
    
    # Load all posts
    all_posts = load_posts()
    
    # Build organized sections with actual post data
    sections_with_posts = []
    for section in hub_config['sections']:
        section_posts = []
        for post_slug in section['posts']:
            post = next((p for p in all_posts if p['slug'] == post_slug), None)
            if post:
                section_posts.append(post)
        
        if section_posts:  # Only include sections that have posts
            sections_with_posts.append({
                'title': section['title'],
                'description': section['description'],
                'posts': section_posts
            })
    
    # Get all posts for this hub's tags (for "More Posts" section)
    related_posts = [p for p in all_posts if any(tag in hub_config['related_tags'] for tag in p['tags'])]
    # Remove duplicates that are already in sections
    section_slugs = [slug for section in hub_config['sections'] for slug in section['posts']]
    additional_posts = [p for p in related_posts if p['slug'] not in section_slugs][:5]
    
    # Generate hub-specific CTA data
    cta_data = get_hub_cta_data(slug)
    
    site_url = app.config.get('SITE_URL', 'https://azure-noob.com')
    canonical_url = f"{site_url}{url_for('hub_page', slug=slug)}"
    
    return render_template('hub.html',
                         hub=hub_config,
                         sections=sections_with_posts,
                         additional_posts=additional_posts,
                         cta_data=cta_data,
                         canonical_url=canonical_url,
                         page_title=f"{hub_config['title']} - Azure Noob",
                         meta_description=hub_config.get('subtitle', ''))

def get_hub_cta_data(hub_slug):
    """Generate CTA configuration for each hub."""
    cta_configs = {
        'finops': {
            'gradient_start': '#10b981',
            'gradient_end': '#059669',
            'emoji': '💰',
            'title': 'Stop Guessing at Azure Costs',
            'subtitle': 'Get the complete Azure FinOps Framework with everything you need to make cost management actually work.',
            'bullets': [
                'Cost allocation templates finance trusts',
                'Tag governance policies that teams follow',
                'Showback dashboards with business context',
                'KQL queries for cost analysis at scale'
            ],
            'cta_text': 'Download FinOps Framework',
            'cta_url': '/static/downloads/Azure-Integration-Assessment-Framework.xlsx',
            'cta_color': '#10b981',
            'reassurance': 'Excel template • KQL queries included • No email required'
        },
        'kql': {
            'gradient_start': '#7c3aed',
            'gradient_end': '#5b21b6',
            'emoji': '🔍',
            'title': 'Stop Rewriting the Same KQL Queries',
            'subtitle': 'Get 45+ production-ready KQL queries you can copy-paste today.',
            'bullets': [
                'VM inventory across all subscriptions',
                'Cost analysis with tag joins',
                'Security compliance audits',
                'Performance optimization patterns'
            ],
            'cta_text': 'Download Complete Query Library',
            'cta_url': '/static/downloads/KQL-Query-Library-Complete.pdf',
            'cta_color': '#7c3aed',
            'reassurance': 'PDF format • Production-tested • No email required'
        },
        'governance': {
            'gradient_start': '#0078d4',
            'gradient_end': '#003d6b',
            'emoji': '🎯',
            'title': 'Make Governance Teams Actually Follow',
            'subtitle': 'Get the tag governance framework that enforces compliance without creating bureaucracy.',
            'bullets': [
                'Tag taxonomy teams understand',
                'Azure Policy templates for auto-enforcement',
                'Compliance dashboards that show trends',
                'Migration to governance best practices'
            ],
            'cta_text': 'Get Governance Framework',
            'cta_url': '/static/downloads/Azure-Integration-Assessment-Framework.xlsx',
            'cta_color': '#0078d4',
            'reassurance': 'Excel + PowerShell • Battle-tested • No email required'
        },
        'monitoring': {
            'gradient_start': '#f59e0b',
            'gradient_end': '#d97706',
            'emoji': '📊',
            'title': 'Build Dashboards Teams Actually Use',
            'subtitle': 'Get workbook templates and dashboard patterns that answer questions instead of raising them.',
            'bullets': [
                'Azure Monitor Workbook templates',
                'KQL queries for operational metrics',
                'Dashboard design patterns',
                'Alerting that drives action'
            ],
            'cta_text': 'Get Dashboard Templates',
            'cta_url': '/static/downloads/KQL-Query-Library-Complete.pdf',
            'cta_color': '#f59e0b',
            'reassurance': 'JSON workbooks • Deployment ready • No email required'
        },
        'migration': {
            'gradient_start': '#06b6d4',
            'gradient_end': '#0891b2',
            'emoji': '☁️',
            'title': 'Stop. Don\'t Migrate Yet.',
            'subtitle': 'Answer 55 questions about each application before touching Azure Migrate.',
            'bullets': [
                'Application assessment questionnaire',
                'Dependency mapping framework',
                'Licensing compliance checklist',
                'Week-by-week migration timeline'
            ],
            'cta_text': 'Get Migration Assessment Framework',
            'cta_url': '/static/downloads/Azure-Integration-Assessment-Framework.xlsx',
            'cta_color': '#06b6d4',
            'reassurance': 'Excel template • Complete instructions • No email required'
        },
        'arc': {
            'gradient_start': '#8b5cf6',
            'gradient_end': '#6d28d9',
            'emoji': '🌉',
            'title': 'Fix Your Arc Ghost Registration Problem',
            'subtitle': 'Detect and clean up Azure Arc registrations that don\'t match actual VMs.',
            'bullets': [
                'Ghost registration detection script',
                'VMware RVTools reconciliation',
                'Arc deployment best practices',
                'Private Link architecture guide'
            ],
            'cta_text': 'Get Arc Ghost Detector',
            'cta_url': '/static/downloads/KQL-Query-Library-Complete.pdf',
            'cta_color': '#8b5cf6',
            'reassurance': 'Python script • Production-tested • No email required'
        },
        'automation': {
            'gradient_start': '#ef4444',
            'gradient_end': '#b91c1c',
            'emoji': '⚡',
            'title': 'Stop Building Custom Scripts for Everything',
            'subtitle': 'Get production-ready automation tools that eliminate repetitive Azure admin work.',
            'bullets': [
                'IPAM tool for IP address management',
                'Service inventory across subscriptions',
                'Dashboard generator for workbooks',
                'Logic App templates for workflows'
            ],
            'cta_text': 'Get Automation Toolkit',
            'cta_url': '/static/downloads/Azure-Integration-Assessment-Framework.xlsx',
            'cta_color': '#ef4444',
            'reassurance': 'PowerShell + Python • GitHub repos • No email required'
        },
        'ai': {
            'gradient_start': '#ec4899',
            'gradient_end': '#9333ea',
            'emoji': '🤖',
            'title': 'Understand Azure OpenAI Costs Before Your $50K Bill',
            'subtitle': 'Get the pricing calculator and cost optimization guide that prevents AI budget disasters.',
            'bullets': [
                'Azure OpenAI pricing calculator',
                'Token consumption estimator',
                'Cost optimization strategies',
                'RAG implementation cost model'
            ],
            'cta_text': 'Get OpenAI Cost Calculator',
            'cta_url': '/static/downloads/KQL-Query-Library-Complete.pdf',
            'cta_color': '#ec4899',
            'reassurance': 'Excel calculator • Real production costs • No email required'
        },
        'terraform': {
            'gradient_start': '#7B42BC',
            'gradient_end': '#5A32A3',
            'emoji': '🏗️',
            'title': 'Stop Writing Terraform Without CI/CD',
            'subtitle': 'Get complete Azure DevOps pipeline templates for production Terraform deployments.',
            'bullets': [
                'Complete build and release YAML pipelines',
                'Remote state backend configuration',
                'Branch policy templates for approvals',
                'Troubleshooting guide for common failures'
            ],
            'cta_text': 'Get Terraform Pipeline Templates',
            'cta_url': '/static/downloads/Azure-Integration-Assessment-Framework.xlsx',
            'cta_color': '#7B42BC',
            'reassurance': 'Azure DevOps YAML • Production-tested • No email required'
        },
        'security': {
            'gradient_start': '#dc2626',
            'gradient_end': '#991b1b',
            'emoji': '🔒',
            'title': 'Pass Your SOC 2 Audit on the First Try',
            'subtitle': 'Get step-by-step SOC 2 compliance guides that auditors actually accept.',
            'bullets': [
                'Activity Log configuration scripts with audit-ready documentation',
                'Entra ID audit log setup for continuous compliance monitoring',
                'Azure Policy templates for automated compliance enforcement',
                'Evidence collection checklists that satisfy SOC 2 controls'
            ],
            'cta_text': 'Download SOC 2 Implementation Guide',
            'cta_url': '/static/downloads/Azure-Integration-Assessment-Framework.xlsx',
            'cta_color': '#dc2626',
            'reassurance': 'PowerShell scripts • Audit checklists • No email required'
        },
    }
    
    return cta_configs.get(hub_slug, cta_configs['finops'])  # Default to finops if slug not found

@app.route('/sitemap.xml')
def sitemap_xml():
    """Generate XML sitemap for SEO."""
    posts = load_posts()

    # Static pages
    pages = [
        {'url': url_for('index', _external=True), 'lastmod': datetime.now().strftime('%Y-%m-%d'), 'priority': '1.0'},
        {'url': url_for('blog_index', _external=True), 'lastmod': datetime.now().strftime('%Y-%m-%d'), 'priority': '0.9'},
        {'url': url_for('hubs_index', _external=True), 'lastmod': datetime.now().strftime('%Y-%m-%d')},
        {'url': url_for('tags_index', _external=True), 'lastmod': datetime.now().strftime('%Y-%m-%d')},
        {'url': url_for('start_here', _external=True), 'lastmod': datetime.now().strftime('%Y-%m-%d')},
        {'url': url_for('about', _external=True), 'lastmod': datetime.now().strftime('%Y-%m-%d')},
    ]
    
    # Add hub pages
    for hub_slug in get_all_hubs().keys():
        pages.append({
            'url': url_for('hub_page', slug=hub_slug, _external=True),
            'lastmod': datetime.now().strftime('%Y-%m-%d')
        })

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

    # Generate XML directly
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for page in pages:
        xml_content += '  <url>\n'
        xml_content += f'    <loc>{page["url"]}</loc>\n'
        xml_content += f'    <lastmod>{page["lastmod"]}</lastmod>\n'
        if 'priority' in page:
            xml_content += f'    <priority>{page["priority"]}</priority>\n'
        xml_content += '  </url>\n'

    xml_content += '</urlset>'

    response = app.response_class(
        xml_content,
        mimetype='application/xml'
    )
    return response

@app.route('/robots.txt')
def robots():
    """Generate robots.txt file."""
    robots_content = """User-agent: *
Allow: /

# Don't index API endpoint
Disallow: /search.json

# AI crawlers - explicitly allowed for GEO/AEO visibility
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Bytespider
Allow: /

User-agent: CCBot
Allow: /

Sitemap: https://azure-noob.com/sitemap.xml"""

    response = app.response_class(
        robots_content,
        mimetype='text/plain'
    )
    return response

@app.route('/rss.xml')
def rss_feed():
    """Generate RSS feed (legacy location)."""
    posts = load_posts()[:10]  # Latest 10 posts

    # Generate RSS XML directly
    rss_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    rss_content += '<rss version="2.0">\n'
    rss_content += '  <channel>\n'
    rss_content += f'    <title>{app.config["SITE_NAME"]}</title>\n'
    rss_content += f'    <description>{app.config["SITE_TAGLINE"]}</description>\n'
    rss_content += f'    <link>{url_for("index", _external=True)}</link>\n'
    rss_content += '    <language>en-us</language>\n'

    for post in posts:
        rss_content += '    <item>\n'
        rss_content += f'      <title>{post["title"]}</title>\n'
        rss_content += f'      <description>{post["summary"]}</description>\n'
        rss_content += f'      <link>{url_for("blog_post", slug=post["slug"], _external=True)}</link>\n'
        rss_content += f'      <pubDate>{post["date"].strftime("%a, %d %b %Y %H:%M:%S +0000")}</pubDate>\n'
        rss_content += f'      <guid>{url_for("blog_post", slug=post["slug"], _external=True)}</guid>\n'
        rss_content += '    </item>\n'

    rss_content += '  </channel>\n'
    rss_content += '</rss>'

    response = app.response_class(
        rss_content,
        mimetype='application/rss+xml'
    )
    return response

@app.route('/feed.xml')
def feed():
    """Generate RSS feed for blog posts (modern standard location)."""
    posts = load_posts()
    posts = sorted(posts, key=lambda x: x['date'], reverse=True)[:20]  # Last 20 posts
    
    from flask import make_response, render_template_string
    
    rss_template = '''<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
    <title>{{ site_name }}</title>
    <link>{{ site_url }}</link>
    <description>{{ site_tagline }}</description>
    <language>en-us</language>
    <lastBuildDate>{{ now().strftime('%a, %d %b %Y %H:%M:%S +0000') }}</lastBuildDate>
    <atom:link href="{{ site_url }}/feed.xml" rel="self" type="application/rss+xml" />
    {% for post in posts %}
    <item>
        <title>{{ post.title }}</title>
        <link>{{ site_url }}/blog/{{ post.slug }}</link>
        <guid>{{ site_url }}/blog/{{ post.slug }}</guid>
        <pubDate>{{ post.date.strftime('%a, %d %b %Y %H:%M:%S +0000') }}</pubDate>
        <description><![CDATA[{{ post.summary }}]]></description>
    </item>
    {% endfor %}
</channel>
</rss>
'''
    
    xml = render_template_string(
        rss_template,
        posts=posts,
        site_name=app.config['SITE_NAME'],
        site_url=app.config['SITE_URL'],
        site_tagline=app.config['SITE_TAGLINE'],
        now=now
    )
    
    response = make_response(xml)
    response.headers['Content-Type'] = 'application/rss+xml; charset=utf-8'
    return response

# Template filters
@app.template_filter('dateformat')
def dateformat(date, format='%B %d, %Y'):
    """Format date for templates."""
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')
    return date.strftime(format)

@app.template_filter('slugify_tag')
def slugify_tag_filter(tag):
    """Template filter version of slugify_tag for consistent URL generation."""
    return slugify_tag(tag)

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
    """Inject navigation data and site config into all templates."""
    return {
        'nav_items': [
            {'name': 'Home', 'url': url_for('index')},
            {'name': 'Blog', 'url': url_for('blog_index')},
            {'name': 'Content Hubs', 'url': url_for('hubs_index')},
            {'name': 'Start Here', 'url': url_for('start_here')},
            {'name': 'Tags', 'url': url_for('tags_index')},
            {'name': 'About', 'url': url_for('about')},
            {'name': 'Search', 'url': url_for('search')},
        ],
        'site_name': app.config.get('SITE_NAME', 'Azure Noob'),
        'site_tagline': app.config.get('SITE_TAGLINE', "Don't be a Noob"),
        'SITE_URL': app.config.get('SITE_URL', 'https://azure-noob.com'),
        'hub_nav': get_hub_navigation()
    }

@app.template_global()
def now():
    """Make current datetime available to templates."""
    return datetime.now()

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors with smart redirect page."""
    return render_template('404.html'), 404

def build_tags():
    """Build tag pages for frozen site generation."""
    tags = get_all_tags()  # Already returns slugified tags
    posts = load_posts()

    # Group posts by slugified tag
    tag_posts = {}
    for tag_slug in tags:
        # Find all posts that have a tag matching this slug
        tag_posts[tag_slug] = [p for p in posts if any(slugify_tag(t) == tag_slug for t in p['tags'])]

    return tag_posts

if __name__ == '__main__':
    app.run(debug=True)
