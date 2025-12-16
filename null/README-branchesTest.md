# 📝 Branch naming

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Branch naming`

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
     - `regex`: `.*...`
     - `min_length`: `10...`
     - `max_length`: `100...`

4. **Debug extracted ticket**
   - 💻 Run: `BRANCH_NAME="${GITHUB_REF#refs/heads/}"...`

5. **Debug Jira API call**
   - 💻 Run: `BRANCH_NAME="${GITHUB_REF#refs/heads/}"...`

6. **Extract Jira Ticket Key**
   - 💻 Run: `BRANCH_NAME="${GITHUB_REF#refs/heads/}"...`

7. **Validate Jira Ticket Exists**
   - 💻 Run: `echo "Checking Jira ticket: ${{ steps.extract.outputs.ticket...`

8. **Comment on PR if branch name is invalid**
   - 📦 Action: `marocchino/sticky-pull-request-comment@v2`
   - ⚙️ Config:
     - `message`: `⚠️ **Branch name does not follow the convention!**...`

---

*This documentation is auto-generated. Do not edit manually.*
