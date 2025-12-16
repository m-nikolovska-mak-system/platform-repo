# 📝 Create Jira Task on App Change

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Create Jira Task on App Change`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `create-jira`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Checkout repository (full)**
   - 📦 Action: `actions/checkout@v4`
   - ⚙️ Config:
     - `fetch-depth`: `0...`

2. **Gather changed files**
   - 💻 Run: `# If this is the first push (no before SHA) list all files i...`

3. **Check for app file changes**
   - 💻 Run: `FILES="${{ steps.changes.outputs.files }}"...`

4. **Create Jira issue when app files changed**
   - 💻 Run: `set -e...`

5. **Upload created issue metadata**
   - 📦 Action: `actions/upload-artifact@v4`
   - ⚙️ Config:
     - `name`: `jira-issue-info...`
     - `path`: `issue_info.txt...`

---

*This documentation is auto-generated. Do not edit manually.*
