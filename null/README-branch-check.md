# 📝 Branch Name Check

**Generated:** 2025-11-26 12:28:06

---

## Overview

**Workflow Name:** `Branch Name Check`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `check-branch`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Step 1**
   - 📦 Action: `actions/checkout@v4`

2. **Get branch name**
   - 💻 Run: `# Try multiple methods to get branch name...`

3. **Check branch naming convention**
   - 💻 Run: `branch="${{ steps.branch.outputs.branch }}"...`

4. **Additional branch checks**
   - 💻 Run: `branch="${{ steps.branch.outputs.branch }}"...`

---

*This documentation is auto-generated. Do not edit manually.*
