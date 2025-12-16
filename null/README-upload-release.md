# 📝 Upload Release Artifact

**Generated:** 2025-11-26 12:28:06

---

## Overview

**Workflow Name:** `Upload Release Artifact`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `upload`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Download installer artifact**
   - 📦 Action: `actions/download-artifact@v4`
   - ⚙️ Config:
     - `name`: `setup-installer...`
     - `path`: `./release-assets...`

2. **Verify artifact exists**
   - 💻 Run: `echo "=== Files in release-assets ==="...`

3. **Upload to GitHub Release**
   - 📦 Action: `softprops/action-gh-release@v2`
   - ⚙️ Config:
     - `files`: `./release-assets/*.exe...`
     - `tag_name`: `${{ inputs.tag_name }}...`

---

*This documentation is auto-generated. Do not edit manually.*
