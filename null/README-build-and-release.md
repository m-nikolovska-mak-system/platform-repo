# 📝 Build & Release Java App

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Build & Release Java App`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `build_jar`

**Runner:** `ubuntu-latest`

**Job Outputs:**

- `jar_path`: `${{ steps.build.outputs.jar_path }}`
- `jar_cache_key`: `${{ steps.build.outputs.jar_cache_key }}`

**Steps:**

1. **Checkout code**
   - 📦 Action: `actions/checkout@v4`

2. **Build JAR**
   - 📦 Action: `m-nikolovska-mak-system/reusable-actions-library/.github/workflows/build-jar.yml@main`
   - ⚙️ Config:
     - `release_tag`: `${{ github.event.release.tag_name || 'dev' }}...`
     - `gradle_task`: `${{ env.GRADLE_TASK }}...`
     - `java_version`: `${{ env.JAVA_VERSION }}...`

### `detect_iss`

**Runner:** `ubuntu-latest`

**Job Outputs:**

- `setup_script`: `${{ steps.detect.outputs.setup_script }}`

**Steps:**

1. **Checkout code**
   - 📦 Action: `actions/checkout@v4`

2. **Detect ISS setup script**
   - 📦 Action: `m-nikolovska-mak-system/reusable-actions-library/.github/workflows/detect-setup-script.yml@main`
   - ⚙️ Config:
     - `pattern`: `**/*.iss...`
     - `fail_if_missing`: `True...`

### `validate_inputs`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Validate JAR cache key**
   - 💻 Run: `if [ -z "${{ needs.build_jar.outputs.jar_cache_key }}" ]; th...`

2. **Validate JAR path**
   - 💻 Run: `if [ -z "${{ needs.build_jar.outputs.jar_path }}" ]; then...`

### `build_installer`

**Runner:** `ubuntu-latest`

**Job Outputs:**

- `installer_artifact_name`: `${{ steps.installer.outputs.installer_artifact_name }}`

**Steps:**

1. **Checkout code**
   - 📦 Action: `actions/checkout@v4`

2. **Build installer**
   - 📦 Action: `m-nikolovska-mak-system/reusable-actions-library/.github/workflows/build-installer.yml@main`
   - ⚙️ Config:
     - `setup_script`: `${{ needs.detect_iss.outputs.setup_script }}...`
     - `jar_path`: `${{ needs.build_jar.outputs.jar_path }}...`
     - `jar_cache_key`: `${{ needs.build_jar.outputs.jar_cache_key }}...`

### `upload_release`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Checkout code**
   - 📦 Action: `actions/checkout@v4`

2. **Upload to release**
   - 📦 Action: `m-nikolovska-mak-system/reusable-actions-library/.github/workflows/upload-release.yml@main`
   - ⚙️ Config:
     - `tag_name`: `${{ github.event.release.tag_name }}...`
     - `artifact_name`: `${{ needs.build_installer.outputs.installer_artifa...`

### `notify_success`

**Calls:** `m-nikolovska-mak-system/reusable-actions-library/.github/workflows/teams-notifier.yml@main`

### `notify_failure`

**Calls:** `m-nikolovska-mak-system/reusable-actions-library/.github/workflows/teams-notifier.yml@main`

---

*This documentation is auto-generated. Do not edit manually.*
