# Azure Noob Blog

**Practical Azure guidance for real-world administrators**

This is the codebase for [azure-noob.com](https://azure-noob.com) - a technical blog focused on solving actual Azure problems with working solutions, not marketing fluff.

## What You'll Find Here

**Real Problems, Real Solutions:**
- KQL queries that actually work in production
- Azure cost management strategies that save money
- Step-by-step guides you can implement Monday morning
- Governance frameworks based on enterprise experience

**Target Audience:**
- Windows administrators moving to Azure
- IT professionals managing Azure environments  
- Anyone who needs practical Azure knowledge without the buzzwords

## Technical Stack

**Built with Flask + Frozen-Flask for simplicity and performance:**

```
├── app.py                 # Flask app for local development
├── freeze.py              # Generates static site for deployment  
├── posts/                 # Markdown blog posts with YAML front matter
├── templates/             # Jinja2 templates for layout
├── static/                # CSS, images, and assets
├── docs/                  # Generated static site (served by GitHub Pages/Netlify)
└── scripts/               # Helper scripts for publishing
```

## Writing Workflow

**Simple process for adding new content:**

1. **Create post:** `posts/YYYY-MM-DD-your-topic.md`
2. **Add YAML front matter:**
   ```yaml
   ---
   title: "Your Post Title"
   date: 2025-09-23
   summary: "Brief description for SEO and index pages"
   tags: ["Azure", "KQL", "FinOps"]
   cover: "/static/images/hero/your-image.png"
   ---
   ```
3. **Write in Markdown** with full code syntax highlighting
4. **Publish:** `git push` (auto-deploys via Netlify)

## Local Development

**Run locally for preview:**

```bash
# Install dependencies
pip install -r requirements.txt

# Start development server
flask run

# Visit http://127.0.0.1:5000
```

**Generate static site:**
```bash
python freeze.py
```

## Content Philosophy

**"You think it's expensive to hire an expert? Try hiring a noob."**

This blog bridges the gap between expensive consultants and undertrained staff. We provide enterprise-grade solutions with approachable explanations.

**Focus Areas:**
- **FinOps & Cost Management** - Real strategies for controlling Azure spend
- **Governance & Compliance** - Practical frameworks that actually work  
- **KQL & Monitoring** - Queries and dashboards for day-to-day operations
- **Migration & Modernization** - Windows to Azure transition guidance

## Contributing

**Found a bug in a query? Have a better approach? Contributions welcome!**

- **Issues:** Report problems or suggest content topics
- **Pull Requests:** Fix typos, improve code, add examples
- **Content Ideas:** What Azure problems are you facing?

## About

Written by enterprise IT professionals who understand that administrators need **practical solutions**, not theoretical frameworks. Content based on real-world implementations and lessons learned in production environments.

**Connect:**
- **Website:** [azure-noob.com](https://azure-noob.com)
- **Email:** david@azure-noob.com
- **GitHub:** Issues and contributions welcome

---

*Built for administrators, by an administrator. No marketing fluff, no vendor pitches, just solutions that work.*