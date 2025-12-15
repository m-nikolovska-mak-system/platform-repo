# 📝 Simple README Generator

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Simple README Generator`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `generate-readme`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Checkout**
   - 📦 Action: `actions/checkout@v4`
   - ⚙️ Config:
     - `token`: `${{ secrets.GITHUB_TOKEN }}...`

2. **Select workflow file**
   - 💻 Run: `echo "workflow_file=.github/workflows/build-installer.yml" >...`

3. **Ensure docs folder exists**
   - 💻 Run: `mkdir -p docs...`

4. **Prepare initial README if needed**
   - 💻 Run: `FILE=docs/README-${{ steps.select.outputs.basename }}.md...`

5. **Run auto-doc**
   - 📦 Action: `tj-actions/auto-doc@v3`
   - ⚙️ Config:
     - `filename`: `${{ steps.select.outputs.workflow_file }}...`
     - `reusable`: `True...`
     - `output`: `docs/README-${{ steps.select.outputs.basename }}.m...`

6. **Commit README changes**
   - 📦 Action: `stefanzweifel/git-auto-commit-action@v5`
   - ⚙️ Config:
     - `commit_message`: `docs: auto-generate README for ${{ steps.select.ou...`
     - `file_pattern`: `docs/*...`

7. **Show result**
   - 💻 Run: `echo "==== README OUTPUT ===="...`

---

*This documentation is auto-generated. Do not edit manually.*
