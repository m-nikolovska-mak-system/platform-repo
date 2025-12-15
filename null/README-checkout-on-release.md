# 📝 Checkout on Release

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Checkout on Release`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `checkout`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Checkout code at release tag**
   - 📦 Action: `actions/checkout@v4`
   - ⚙️ Config:
     - `ref`: `${{ github.event.release.tag_name }}...`

2. **Show current commit and tag**
   - 💻 Run: `echo "Checked out tag: ${{ github.event.release.tag_name }}"...`

---

*This documentation is auto-generated. Do not edit manually.*
