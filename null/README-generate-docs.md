# 📝 Generate workflow docs

**Generated:** 2025-11-26 12:28:06

---

## Overview

**Workflow Name:** `Generate workflow docs`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `build-doc`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Checkout repo**
   - 📦 Action: `actions/checkout@v4`

2. **Generate README with auto-doc**
   - 📦 Action: `tj-actions/auto-doc@v3`
   - ⚙️ Config:
     - `file`: `${{ github.event.inputs.filename }}...`
     - `output`: `${{ github.event.inputs.output }}...`

3. **Commit generated docs**
   - 📦 Action: `EndBug/add-and-commit@v9`
   - ⚙️ Config:
     - `author_name`: `github-actions[bot]...`
     - `author_email`: `41898282+github-actions[bot]@users.noreply.github....`
     - `message`: `chore(docs): update workflow docs for ${{ github.e...`

---

*This documentation is auto-generated. Do not edit manually.*
