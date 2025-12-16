# 📝 Generate Workflow Documentation

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Generate Workflow Documentation`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `generate-docs`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Step 1**
   - 📦 Action: `actions/checkout@v4`
   - ⚙️ Config:
     - `fetch-depth`: `0...`

2. **Setup Node**
   - 📦 Action: `actions/setup-node@v4`
   - ⚙️ Config:
     - `node-version`: `20...`

3. **Install dependencies**
   - 💻 Run: `npm install...`

4. **Generate workflow docs**
   - 💻 Run: `node scripts/generate-workflow-docs.js...`

5. **Create Pull Request for updated workflow docs**
   - 📦 Action: `peter-evans/create-pull-request@v6`
   - ⚙️ Config:
     - `commit-message`: `docs: auto-update workflow READMEs...`
     - `title`: `docs: auto-update workflow READMEs...`
     - `body`: `This PR updates the documentation for workflows in...`

---

*This documentation is auto-generated. Do not edit manually.*
