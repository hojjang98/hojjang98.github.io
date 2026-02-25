# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**HJ's Security Note** is a personal Hugo static site blog focused on security law, governance, and practical security training. Content is written in Korean and deployed to GitHub Pages at https://hojjang98.github.io/.

## Commands

```bash
# Local development server with live reload
hugo server

# Production build (minified)
hugo --minify

# Create a new post from archetype template
hugo new content/<section>/<filename>.md
```

Deployment is fully automated via GitHub Actions on every push to `main` — no manual deploy step needed.

## Architecture

- **Generator**: Hugo v0.146.0 (extended), theme: PaperMod
- **Config split**: `hugo.toml` (root, global settings) + `config/_default/` (languages, menus, params)
- **Content**: All in `content/` as Markdown with TOML front matter
- **Custom CSS**: `assets/css/extended/custom.css` (loaded automatically by PaperMod's asset pipeline)
- **Build output**: `public/` directory (do not edit manually; regenerated on each build)
- **Static assets**: `static/` (copied as-is to `public/` root)

## Content Structure

```
content/
├── about.md                   # Author intro page
├── cyber_law_study/           # Korean security law study notes
│   ├── 01_기본법률/           # Core statutes (PIPA, Network Act, etc.)
│   └── 02_산업별규제/         # Industry-specific regulations
├── daily_logs/                # SK Shields Rookies training logs (by week)
├── paper_review/              # Academic paper summaries
└── security-issues-analysis/  # Security incident/issue analysis
```

## Front Matter Convention

All posts use TOML front matter (triple-dash fences with TOML syntax):

```markdown
---
title: "Post Title"
date: 2026-02-25
categories: ["cyber-law-study"]
tags: ["태그1", "태그2"]
draft: false
summary: "One-line summary shown in list views."
---
```

Valid category slugs used in menus: `cyber-law-study`, `daily-logs`, `paper-review`, `security-issues-analysis`.

## Key Configuration

- `hugo.toml` — base URL, language (`ko`), theme, output formats (HTML + RSS + JSON for search)
- `config/_default/params.toml` — PaperMod theme options (profile mode, social links, search)
- `config/_default/menus.ko.toml` — Top navigation menu items
- `config/_default/languages.ko.toml` — Korean locale, date format (`2006년 1월 2일`)
- `.github/workflows/hugo.yaml` — CI/CD: installs Hugo 0.146.0 extended, runs `hugo --minify`, deploys to GitHub Pages
