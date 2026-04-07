# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Set up environment (first time)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the development server (localhost:5001)
python app.py

# Run tests
pytest

# Run a single test file
pytest tests/test_auth.py

# Run a single test by name
pytest tests/test_auth.py::test_login
```

## Architecture

**Spendly** is a Flask expense-tracker app targeting the Indian market (₹). It uses server-side rendering via Jinja2 templates — there is no frontend build step, no bundler, and no JS framework.

### Stack
- **Backend:** Flask 3.1.3, SQLite (via `database/db.py`)
- **Frontend:** Jinja2 templates, vanilla CSS/JS (no framework)
- **Testing:** pytest + pytest-flask

### Key files
- `app.py` — all routes live here; runs on port 5001
- `database/db.py` — SQLite helpers: `get_db()`, `init_db()`, `seed_db()` (partially implemented)
- `templates/base.html` — shared layout; all pages extend this
- `static/css/style.css` — single stylesheet; uses CSS variables for the design system (green `#1a472a`, orange `#c17f24`, dark ink, light paper)
- `static/js/main.js` — vanilla JS; currently handles the YouTube modal on the landing page

### Routing pattern
All routes are plain functions in `app.py` returning `render_template(...)`. Placeholder routes return plain strings and are labelled "coming in Step N" — this is an incremental tutorial project.

Current live routes: `/`, `/terms`, `/privacy`, `/register`, `/login`  
Placeholder routes (to be implemented): `/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`

### Database
SQLite connection is set up in `database/db.py`. The schema (users + expenses tables) and `init_db()` / `seed_db()` helpers are the next things to implement. Foreign keys are enabled on every connection.
