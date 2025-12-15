# 📝 Main Build and Release

**Generated:** 2025-11-26 12:28:06

---

## Overview

**Workflow Name:** `Main Build and Release`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `build_jar`

**Calls:** `./.github/workflows/build-jar.yml`

### `detect_iss`

**Calls:** `./.github/workflows/detect-setup-script.yml`

### `build_installer`

**Calls:** `./.github/workflows/build-installer.yml`

### `upload_release`

**Calls:** `./.github/workflows/upload-release.yml`

### `notify-on-failure`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Report failure**
   - 💻 Run: `echo "❌ Workflow failed"...`

---

*This documentation is auto-generated. Do not edit manually.*
