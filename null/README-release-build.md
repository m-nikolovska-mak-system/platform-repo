# 📝 Build and Release

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Build and Release`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `build-jar`

**Calls:** `m-nikolovska-mak-system/reusable-actions-library/.github/workflows/build-jar.yml@main`

### `detect-setup-script`

**Runner:** `ubuntu-latest`

**Job Outputs:**

- `setup_script`: `${{ steps.detect.outputs.script }}`

**Steps:**

1. **Checkout code**
   - 📦 Action: `actions/checkout@v4`
   - ⚙️ Config:
     - `ref`: `${{ github.event.inputs.release_tag || github.even...`

2. **Find .iss script**
   - 💻 Run: `echo "🔍 Looking for Inno Setup script..."...`

### `build-installer`

**Calls:** `m-nikolovska-mak-system/reusable-actions-library/.github/workflows/build-installer.yml@main`

### `upload-to-release`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Download installer artifact**
   - 📦 Action: `actions/download-artifact@v4`
   - ⚙️ Config:
     - `name`: `${{ needs.build-installer.outputs.installer_artifa...`
     - `path`: `./installer...`

2. **Verify installer exists**
   - 💻 Run: `echo "📦 Downloaded artifacts:"...`

3. **Upload installer to GitHub Release**
   - 📦 Action: `softprops/action-gh-release@v2`
   - ⚙️ Config:
     - `files`: `installer/*.exe...`
     - `tag_name`: `${{ github.event.release.tag_name }}...`
     - `fail_on_unmatched_files`: `True...`

4. **Success notification**
   - 💻 Run: `echo "✅ Installer successfully uploaded to release ${{ githu...`

### `test-summary`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Display test results**
   - 💻 Run: `echo "=========================================="...`

---

*This documentation is auto-generated. Do not edit manually.*
