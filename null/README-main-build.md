# 📝 Main Build and Release

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Main Build and Release`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `build-jar`

**Runner:** `ubuntu-latest`

**Job Outputs:**

- `jar_cache_key`: `${{ steps.cache-key.outputs.key }}`

**Steps:**

1. **Checkout code**
   - 📦 Action: `actions/checkout@v4`
   - ⚙️ Config:
     - `ref`: `${{ github.event.release.tag_name || 'main' }}...`

2. **Set up Java 17**
   - 📦 Action: `actions/setup-java@v3`
   - ⚙️ Config:
     - `distribution`: `temurin...`
     - `java-version`: `17...`

3. **Make Gradle wrapper executable**
   - 💻 Run: `chmod +x gradlew...`

4. **Cache Gradle dependencies**
   - 📦 Action: `actions/cache@v3`
   - ⚙️ Config:
     - `path`: `~/.gradle/caches ~/.gradle/wrapper ...`
     - `key`: `${{ runner.os }}-gradle-${{ hashFiles('**/*.gradle...`
     - `restore-keys`: `${{ runner.os }}-gradle- ...`

5. **Build JAR with Gradle**
   - 💻 Run: `./gradlew jar --no-daemon...`

6. **Validate JAR**
   - 💻 Run: `jar_file=$(ls build/libs/*.jar 2>/dev/null | head -n 1)...`

7. **Generate cache key**
   - 💻 Run: `echo "key=jar-${{ github.sha }}-${{ github.run_number }}" >>...`

8. **Cache built JAR**
   - 📦 Action: `actions/cache/save@v3`
   - ⚙️ Config:
     - `path`: `build/libs/*.jar...`
     - `key`: `${{ steps.cache-key.outputs.key }}...`

### `detect-setup-script`

**Runner:** `ubuntu-latest`

**Job Outputs:**

- `setup_script`: `${{ steps.detect-iss.outputs.script }}`

**Steps:**

1. **Checkout code**
   - 📦 Action: `actions/checkout@v4`

2. **Detect setup script**
   - 💻 Run: `file=$(ls *.iss 2>/dev/null | head -n 1)...`

### `call-installer`

**Calls:** `m-nikolovska-mak-system/reusable-actions-library/.github/workflows/build-installer.yml@main`

### `upload-to-release`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Download installer artifact**
   - 📦 Action: `actions/download-artifact@v4`
   - ⚙️ Config:
     - `name`: `setup-installer...`
     - `path`: `output...`

2. **Verify installer exists**
   - 💻 Run: `echo "=== Files downloaded ==="...`

3. **Upload installer to GitHub Release**
   - 📦 Action: `softprops/action-gh-release@v2`
   - ⚙️ Config:
     - `files`: `output/*.exe...`
     - `tag_name`: `${{ github.event.release.tag_name }}...`

### `notify-on-failure`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Report failure**
   - 💻 Run: `echo "❌ Workflow failed"...`

---

*This documentation is auto-generated. Do not edit manually.*
