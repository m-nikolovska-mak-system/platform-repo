# 📝 OVA TREBA DA RABOTI Build JAR

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `OVA TREBA DA RABOTI Build JAR`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `build-jar`

**Runner:** `ubuntu-latest`

**Job Outputs:**

- `jar-cache-key`: `${{ steps.cache-key.outputs.key }}`

**Steps:**

1. **Checkout code**
   - 📦 Action: `actions/checkout@v4`
   - ⚙️ Config:
     - `ref`: `${{ github.event.release.tag_name || github.event....`

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
   - 💻 Run: `./gradlew clean jar --no-daemon...`

6. **Upload JAR as artifact**
   - 📦 Action: `actions/upload-artifact@v4`
   - ⚙️ Config:
     - `name`: `app-jar...`
     - `path`: `build/libs/*.jar...`

7. **Generate cache key**
   - 💻 Run: `echo "key=jar-${{ github.sha }}-${{ github.run_number }}" >>...`

8. **Cache built JAR**
   - 📦 Action: `actions/cache/save@v3`
   - ⚙️ Config:
     - `path`: `build/libs/*.jar...`
     - `key`: `${{ steps.cache-key.outputs.key }}...`

### `build-installer`

**Runner:** `windows-latest`

**Steps:**

1. **Checkout repo**
   - 📦 Action: `actions/checkout@v4`
   - ⚙️ Config:
     - `ref`: `${{ github.event.release.tag_name || github.event....`

2. **Download JAR artifact**
   - 📦 Action: `actions/download-artifact@v4`
   - ⚙️ Config:
     - `name`: `app-jar...`
     - `path`: `build/libs...`

3. **Rename JAR to App.jar**
   - 💻 Run: `$jar = Get-ChildItem build\libs\*.jar | Select-Object -First...`

4. **Verify JAR**
   - 💻 Run: `dir build\libs...`

5. **Install Inno Setup**
   - 💻 Run: `choco install innosetup --no-progress -y...`

6. **Build setup.exe**
   - 💻 Run: `& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" setup-scrip...`

7. **Check output folder**
   - 💻 Run: `dir output...`

8. **Upload setup.exe to GitHub Release**
   - 📦 Action: `softprops/action-gh-release@v2`
   - ⚙️ Config:
     - `files`: `output/OneProjectWed-Setup.exe...`
     - `tag_name`: `${{ github.event.release.tag_name }}...`

9. **Upload setup.exe as artifact (for workflow_dispatch)**
   - 📦 Action: `actions/upload-artifact@v4`
   - ⚙️ Config:
     - `name`: `setup-installer...`
     - `path`: `output/OneProjectWed-Setup.exe...`

---

*This documentation is auto-generated. Do not edit manually.*
