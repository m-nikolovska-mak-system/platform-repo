# 📝 Notify on App.java Changes

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Notify on App.java Changes`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `check-file-changes`

**Calls:** `m-nikolovska-mak-system/reusable-actions-library/.github/workflows/check-for-file-changes.yml@main`

### `debug-outputs`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Print check results**
   - 💻 Run: `echo "Job status: ${{ needs.check-file-changes.result }}"...`

### `send-teams-notification`

**Calls:** `m-nikolovska-mak-system/reusable-actions-library/.github/workflows/send-teams-notification-v2.yml@main`

---

*This documentation is auto-generated. Do not edit manually.*
