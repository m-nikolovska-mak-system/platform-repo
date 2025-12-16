# 📝 Build & Release Java App

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Build & Release Java App`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `build_jar`

**Calls:** `m-nikolovska-mak-system/reusable-actions-library/.github/workflows/build-jar.yml@main`

### `detect_iss`

**Calls:** `m-nikolovska-mak-system/reusable-actions-library/.github/workflows/detect-setup-script.yml@main`

### `validate_inputs`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Check jar_cache_key**
   - 💻 Run: `if [ -z "${{ needs.build_jar.outputs.jar_cache_key }}" ]; th...`

### `build_installer`

**Calls:** `m-nikolovska-mak-system/reusable-actions-library/.github/workflows/build-installer.yml@main`

### `upload_release`

**Calls:** `m-nikolovska-mak-system/reusable-actions-library/.github/workflows/upload-release.yml@main`

### `notify_failure`

**Calls:** `m-nikolovska-mak-system/reusable-actions-library/.github/workflows/teams-notifier.yml@main`

---

*This documentation is auto-generated. Do not edit manually.*
