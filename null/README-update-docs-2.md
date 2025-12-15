# 📝 Update Docs for Workflows

**Generated:** 2025-11-26 12:28:06

---

## Overview

**Workflow Name:** `Update Docs for Workflows`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `update-docs`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Step 1**
   - 📦 Action: `actions/checkout@v4`

2. **Generate docs for main action**
   - 📦 Action: `tj-actions/auto-doc@v3`
   - ⚙️ Config:
     - `filename`: `action.yml...`
     - `output`: `README.md...`

3. **Generate docs for reusable workflow**
   - 📦 Action: `tj-actions/auto-doc@v3`
   - ⚙️ Config:
     - `filename`: `.github/workflows/notify-app-changes-v3.yml...`
     - `output`: `docs/reusable.md...`

---

*This documentation is auto-generated. Do not edit manually.*
