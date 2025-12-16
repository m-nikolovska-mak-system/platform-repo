# 📝 Notify Teams on Changes

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Notify Teams on Changes`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `detect-changes`

**Runner:** `ubuntu-latest`

**Job Outputs:**

- `changed_files`: `${{ steps.changes.outputs.files }}`

**Steps:**

1. **Checkout code**
   - 📦 Action: `actions/checkout@v4`
   - ⚙️ Config:
     - `fetch-depth`: `2...`

2. **Get changed files**
   - 💻 Run: `# For push events, compare with previous commit...`

### `notify-teams`

**Calls:** `m-nikolovska-mak-system/reusable-actions-library/.github/workflows/teams-notifier.yml@main`

---

*This documentation is auto-generated. Do not edit manually.*
