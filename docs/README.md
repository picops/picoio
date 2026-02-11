# picoio documentation

## What you need to build and view the docs

### Prerequisites

- **Python 3.13+**
- **Package build deps**: so that `picoio` can be imported (Sphinx autodoc inspects the package).
  - System: e.g. `libzip-dev` on Debian/Ubuntu (for the ZIP extension).
  - Python: install the project in editable mode (see below).
- **Sphinx + theme**: provided by the `dev` extra (`sphinx`, `sphinx-rtd-theme`).

### Build the package then the docs

1. From the repo root, install and build the project:

   ```bash
   uv sync --extra dev
   uv pip install -e .
   ```

   (Or use your project’s usual build steps, e.g. `make build` then `make install`.)

2. Build HTML docs:

   ```bash
   uv run python -m sphinx -b html docs docs/_build/html
   ```

3. Open `docs/_build/html/index.html` in a browser.

### Viewing the version switcher (multi-version)

The sidebar version dropdown is populated from environment variables that **CI sets** when building for GitHub Pages:

- `CURRENT_DOC_VERSION` – current build (e.g. `latest` or `0.0.1`).
- `DOC_VERSIONS` – comma-separated list of versions (e.g. `latest,0.0.1,0.0.0`).
- `GITHUB_PAGES_BASE` – base path for the site (e.g. `/picoio` for `https://<user>.github.io/picoio/`).

To test the switcher locally, run Sphinx with those set, for example:

```bash
export CURRENT_DOC_VERSION=latest
export DOC_VERSIONS=latest,0.0.1
export GITHUB_PAGES_BASE=/picoio
uv run python -m sphinx -b html docs docs/_build/html
```

Then serve `docs/_build/html` with a server that reflects the base path (e.g. under `/picoio/`), or open files directly (switcher links will assume the base path above).

### GitHub Pages (CI)

- The **Docs** workflow (`.github/workflows/docs.yml`) builds Sphinx on push to `main` and on `workflow_dispatch`.
- In the repo: **Settings → Pages → Build and deployment**: set source to **GitHub Actions** so the workflow can deploy.
- After deployment, docs are at `https://<owner>.github.io/<repo>/` (e.g. `https://user.github.io/picoio/`). The root redirects to `latest/` and the sidebar shows a version switcher when multiple versions exist.
