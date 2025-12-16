# 📝 Notify App Changes on Release

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Notify App Changes on Release`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `check_app_change`

**Runner:** `ubuntu-latest`

**Job Outputs:**

- `should_notify`: `${{ steps.check.outputs.should_notify }}`

**Steps:**

1. **Checkout repository**
   - 📦 Action: `actions/checkout@v4`
   - ⚙️ Config:
     - `fetch-depth`: `0...`

2. **Get current release tag**
   - 💻 Run: `echo "tag=${{ github.event.release.tag_name }}" >> $GITHUB_O...`

3. **Get previous tag**
   - 💻 Run: `prev_tag=$(git tag --sort=-creatordate | grep -B1 "${{ steps...`

4. **Check if App.java changed**
   - 💻 Run: `if git diff --name-only ${{ steps.previous_tag.outputs.prev_...`

### `notify`

**Calls:** `./.github/workflows/teams-notif-simple.yml`

---

*This documentation is auto-generated. Do not edit manually.*
