# 📝 🧩 Detect & Act on File Changes

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `🧩 Detect & Act on File Changes`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `check_changes`

**Calls:** `m-nikolovska-mak-system/reusable-actions-library/.github/workflows/check-file-changes.yml@main`

### `run_on_change`

**Runner:** `ubuntu-latest`

**Steps:**

1. **✅ Files changed**
   - 💻 Run: `echo "Changed files:"...`

### `run_on_no_change`

**Runner:** `ubuntu-latest`

**Steps:**

1. **ℹ️ No watched files changed**
   - 💻 Run: `echo "No relevant files changed. Skipping build."...`

---

*This documentation is auto-generated. Do not edit manually.*
