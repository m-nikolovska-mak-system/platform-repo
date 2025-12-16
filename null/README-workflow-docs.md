# 📝 Generate Workflow Docs

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Generate Workflow Docs`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `generate-docs`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Checkout**
   - 📦 Action: `actions/checkout@v4`
   - ⚙️ Config:
     - `fetch-depth`: `0...`

2. **Setup Python**
   - 📦 Action: `actions/setup-python@v5`
   - ⚙️ Config:
     - `python-version`: `3.11...`

3. **Install dependencies**
   - 💻 Run: `pip install pyyaml...`

4. **Generate workflow documentation**
   - 💻 Run: `python scripts/workflow_docs.py...`

5. **Show generated docs**
   - 💻 Run: `echo "==== GENERATED WORKFLOW DOCS ===="...`

6. **Create Pull Request**
   - 📦 Action: `peter-evans/create-pull-request@v6`
   - ⚙️ Config:
     - `token`: `${{ secrets.GITHUB_TOKEN }}...`
     - `commit-message`: `docs: auto-generate workflow documentation...`
     - `title`: `📝 Update workflow documentation...`

---

*This documentation is auto-generated. Do not edit manually.*
