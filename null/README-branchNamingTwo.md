# 📝 Branch Name Validation

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Branch Name Validation`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `branch-naming-rules`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Checkout code**
   - 📦 Action: `actions/checkout@v3`

2. **Validate branch name on create**
   - 💻 Run: `BRANCH_NAME="${GITHUB_REF#refs/heads/}"...`

3. **Validate branch name on push**
   - 📦 Action: `deepakputhraya/action-branch-name@master`
   - ⚙️ Config:
     - `regex`: `^(hot-fix-)?[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*-ERP-[0-9]...`
     - `min_length`: `10...`
     - `max_length`: `100...`

4. **Extract Jira Ticket Key**
   - 💻 Run: `BRANCH_NAME="${GITHUB_REF#refs/heads/}"...`

5. **Validate Jira Ticket Exists**
   - 💻 Run: `echo "Checking Jira ticket: ${{ steps.extract.outputs.ticket...`

6. **Notify Microsoft Teams on failure**
   - 💻 Run: `curl -H 'Content-Type: application/json' \...`

7. **Create GitHub Issue on violation**
   - 💻 Run: `BRANCH_NAME="${GITHUB_REF#refs/heads/}"...`

8. **Comment on PR if branch name is invalid**
   - 📦 Action: `marocchino/sticky-pull-request-comment@v2`
   - ⚙️ Config:
     - `message`: `⚠️ **Branch name does not follow the convention or...`

---

*This documentation is auto-generated. Do not edit manually.*
