# 📝 Notify on App.java Changes

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Notify on App.java Changes`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `check_file_changes`

**Calls:** `m-nikolovska-mak-system/reusable-actions-library/.github/workflows/check-for-file-changes.yml@main`

### `debug_outputs`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Print outputs from check_file_changes**
   - 💻 Run: `echo "Files changed: ${{ needs.check_file_changes.outputs.fi...`

### `send_teams_notification`

**Calls:** `m-nikolovska-mak-system/reusable-actions-library/.github/workflows/send-teams-notification.yml@main`

---

*This documentation is auto-generated. Do not edit manually.*
