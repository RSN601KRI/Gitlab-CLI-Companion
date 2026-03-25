<h1 align="center">GitLab DevOps Companion CLI (glc)</h1>
<p align="center">
  <b>AI-powered DevOps Co-pilot for Migration, Security, Docs & Code Review</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Built%20with-Python-blue" />
  <img src="https://img.shields.io/badge/CLI-Typer-green" />
  <img src="https://img.shields.io/badge/UI-Streamlit-red" />
  <img src="https://img.shields.io/badge/API-GitLab-orange" />
  <img src="https://img.shields.io/badge/Status-Active-success" />
</p>

## The Problem

Modern DevOps is **fragmented**:

- Jenkins → GitLab migration is manual  
- Documentation gets outdated  
- Security risks go unnoticed  
- Code review lacks context  

> Developers waste time switching tools instead of building.

## The Solution

**`glc` = One CLI. Total DevOps Automation.**

```bash
glc migrate   # CI/CD Migration
glc docs      # Auto Documentation
glc scan      # Security Analysis
glc review    # MR Risk Intelligence
glc health    # Repo Health Dashboard
````

## Demo Workflow (1 Command Story)

```bash
# Migrate → Document → Scan → Review → Monitor
glc migrate && glc docs && glc scan && glc review --post && glc health
```

## Features

### CI/CD Migration

Convert Jenkins pipelines into GitLab CI automatically.

### Smart Documentation

Auto-generate:

* README
* CONTRIBUTING
* Architecture docs

### Security Scanner

* Detect secrets
* Identify risky configs
* Generate security score

### MR Intelligence

* Analyse code changes
* Predict impact
* Calculate blast radius
* Post insights directly to GitLab

### Repo Health Dashboard

A unified DevOps scorecard:

* Security ✔
* Docs ✔
* Pipelines ✔
* Risk ✔

## Live Dashboard

```bash
streamlit run dashboard.py
```

## How It Works

We built a **Knowledge Graph Engine** that connects:

* Files
* Pipelines
* Documentation
* Relationships

This shared context powers:

* smarter migration
* accurate risk analysis
* intelligent documentation

## Installation

```bash
git clone https://github.com/your-username/gitlab-devops-companion.git
cd gitlab-devops-companion

python -m venv .venv
.\.venv\Scripts\activate

pip install -r requirements.txt
pip install -e .
```

## GitLab Integration

```env
GITLAB_TOKEN=your_token
GITLAB_URL=https://gitlab.com/api/v4
GITLAB_PROJECT_ID=your_project_id
GITLAB_MR_IID=your_mr_id
```

## Usage

```bash
python -m glc.main migrate
python -m glc.main docs
python -m glc.main scan
python -m glc.main review --post
python -m glc.main health
```

## Project Structure

```
glc/
├── commands/        # CLI commands
├── integrations/    # GitLab API
├── graph/           # Knowledge Graph
├── main.py          # Entry point

dashboard.py         # Streamlit UI
```

## Why This Stands Out

✅ Unified DevOps workflow
✅ Real GitLab API integration
✅ AI-style risk analysis
✅ CLI + UI combo
✅ Strong demo narrative

## Challenges

* Jenkins → GitLab CI mapping
* CLI packaging issues
* Secure API handling
* Risk scoring logic

## Future Scope

* Auto-detect MR & project
* Webhook-based automation
* AI fix suggestions
* Advanced analytics
* Deploy as SaaS

## 🎥 Demo (Add Your Video Here)

```md
Watch Demo: https://vimeo.com/1176809996?share=copy&fl=sv&fe=ci
```

## Support

If you like this project:

* Star the repo
* Fork it
* Contribute ideas
