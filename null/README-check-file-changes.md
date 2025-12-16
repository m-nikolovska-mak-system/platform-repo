# 📝 Check File Changes

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Check File Changes`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `check`

**Runner:** `ubuntu-latest`

**Job Outputs:**

- `changed`: `${{ steps.detect.outputs.changed }}`
- `files`: `${{ steps.detect.outputs.files }}`
- `current_ref`: `${{ steps.refs.outputs.current }}`

**Steps:**

1. **Checkout repository**
   - 📦 Action: `actions/checkout@v4`
   - ⚙️ Config:
     - `fetch-depth`: `0...`

2. **Resolve refs**
   - 💻 Run: `current="${{ inputs.current_ref }}"...`

3. **Detect changes**
   - 💻 Run: `pattern="${{ inputs.file_pattern }}"...`

---

*This documentation is auto-generated. Do not edit manually.*
