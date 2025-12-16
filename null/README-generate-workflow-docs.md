# 📝 Generate Workflow Docs

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Generate Workflow Docs`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `build-doc`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Step 1**
   - 📦 Action: `actions/checkout@v4`

2. **Ensure output directory exists**
   - 💻 Run: `mkdir -p $(dirname "${{ github.event.inputs.output }}")...`

3. **Generate README with auto-doc**
   - 📦 Action: `tj-actions/auto-doc@v3`
   - ⚙️ Config:
     - `filename`: `${{ github.event.inputs.filename }}...`
     - `output`: `${{ github.event.inputs.output }}...`

4. **Debug git status**
   - 💻 Run: `git status --short...`

5. **Commit generated docs**
   - 📦 Action: `EndBug/add-and-commit@v9`
   - ⚙️ Config:
     - `author_name`: `github-actions[bot]...`
     - `author_email`: `41898282+github-actions[bot]@users.noreply.github....`
     - `message`: `chore(docs): update workflow docs...`

---

*This documentation is auto-generated. Do not edit manually.*
