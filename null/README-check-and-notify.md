# 📝 Detect File Change + MS Teams Notification

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Detect File Change + MS Teams Notification`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `check_changes`

**Calls:** `m-nikolovska-mak-system/reusable-actions-library/.github/workflows/3check-file-changes.yml@main`

### `debug_print`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Show outputs**
   - 💻 Run: `echo "files_changed='${{ needs.check_changes.outputs.files_c...`

### `notify_if_changed`

**Calls:** `m-nikolovska-mak-system/reusable-actions-library/.github/workflows/teams-notifier.yml@main`

---

*This documentation is auto-generated. Do not edit manually.*
