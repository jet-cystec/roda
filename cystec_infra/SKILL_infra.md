---
name: Cystec Infrastructure & CI/CD
description: Standardized CI/CD pipeline and build system for Cystec static sites. Includes GitHub Actions workflow for automated deployment to GitHub Pages and a Python-based build script with safe optimization.
---

# Cystec Infrastructure & CI/CD Skill

This skill provides the standard infrastructure setup for Cystec web projects, ensuring consistent, optimized, and automated deployments to GitHub Pages.

## 🏗️ Architecture

- **Hosting:** GitHub Pages
- **Automation:** GitHub Actions
- **Build System:** Custom Python Script (`build_site.py`)
- **Optimization Strategy:** "Soft Minification" (Comments removed, Scripts deferred with protections, Whitespace PRESERVED)

## 📦 Components

### 1. Build Script (`build_site.py`)

Located in: `scripts/build_site.py`

**Features:**
- **Automated Backup:** Creates timestamped backups before building.
- **Safe Minification:** Removes comments using a strict whitelist (only `CONTENT:` preserved) and replaces them with a single space (not newline) to prevent line bloat while maintaining layout safety.
- **Smart Script Optimization:** Adds `defer` to scripts for performance, but **EXCLUDES** critical libraries:
  - `tailwindcss.com` (Avoids race conditions with inline config)
  - `unpkg.com/lucide` (Ensures icons render correctly)
- **Metrics Report:** Displays file size savings after build.

### 2. Deployment Workflow (`deploy.yml`)

Located in: `templates/deploy.yml`

**Features:**
- **Trigger:** Auto-deploys on push to `main` branch.
- **Process:**
  1. Sets up Python env.
  2. Runs `build_site.py`.
  3. Swaps `index.min.html` to `index.html`.
  4. Deploys to `gh-pages` branch.
- **Permissions:** Configured with `contents: write` to allow the bot to push to the branch.

## 🚀 Usage Guide

### Step 1: Initialize Infrastructure

Copy the standard files to your project root:

```bash
# Copy build script
cp .agent/skills/cystec_infra/scripts/build_site.py ./

# Create workflow directory
mkdir -p .github/workflows
cp .agent/skills/cystec_infra/templates/deploy.yml .github/workflows/
```

### Step 2: Configure Git Ignore

Ensure your `.gitignore` excludes the generated build artifacts but allows tracking of the source code. See `examples/gitignore_example`.

```gitignore
# Generated artifacts
index.min.html
backups/
```

### Step 3: GitHub Repository Settings

1. Go to **Settings > Actions > General**.
   - Ensure "Read and write permissions" is enabled (or use the `permissions: contents: write` in the yaml).
2. Go to **Settings > Pages**.
   - **Source:** Deploy from a branch
   - **Branch:** `gh-pages`
   - **Folder:** `/ (root)`

### Step 4: Verify Deployment

Push changes to `main`. The workflow will:
1. Build the site.
2. Publish to `gh-pages`.
3. Your site will be live at `https://<user>.github.io/<repo>/` or your custom domain.

## ⚠️ Critical Safety Notes

**Do NOT enable aggressive HTML whitespace minification.**
Experience with the `ancla` project showed that removing whitespace breaks:
- Tailwind CSS layouts (inline-block spacing).
- DOM structure relied upon by JavaScript.

**Do NOT defer Tailwind or Lucide scripts.**
- Tailwind inline config must run *after* the library loads.
- Lucide icons must initialize *after* the library loads.
The provided `build_site.py` handles these exceptions automatically.
