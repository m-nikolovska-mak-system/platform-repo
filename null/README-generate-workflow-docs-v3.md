# 📝 Generate Workflow Docs

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Generate Workflow Docs`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `docs`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Checkout**
   - 📦 Action: `actions/checkout@v4`

2. **Find all workflow files**
   - 💻 Run: `files=$(ls .github/workflows/*.yml .github/workflows/*.yaml ...`

3. **Install node**
   - 📦 Action: `actions/setup-node@v4`
   - ⚙️ Config:
     - `node-version`: `18...`

4. **Install dependencies**
   - 💻 Run: `npm install js-yaml...`

5. **Generate docs**
   - 💻 Run: `mkdir -p docs/workflows...`

6. **Commit documentation**
   - 📦 Action: `stefanzweifel/git-auto-commit-action@v5`
   - ⚙️ Config:
     - `commit_message`: `auto: update workflow documentation...`
     - `file_pattern`: `docs/workflows/*.md...`

---

*This documentation is auto-generated. Do not edit manually.*
