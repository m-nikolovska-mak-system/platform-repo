# 📝 Build JAR on Release

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Build JAR on Release`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `build`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Checkout code at release tag**
   - 📦 Action: `actions/checkout@v4`
   - ⚙️ Config:
     - `ref`: `${{ github.event.release.tag_name }}...`

2. **Set up Java**
   - 📦 Action: `actions/setup-java@v3`
   - ⚙️ Config:
     - `distribution`: `temurin...`
     - `java-version`: `17...`

3. **Make Gradle executable**
   - 💻 Run: `chmod +x gradlew...`

4. **Build JAR with Gradle**
   - 💻 Run: `./gradlew jar --no-daemon...`

5. **Set cache key**
   - 💻 Run: `echo "cache-key=jar-${{ github.sha }}-${{ github.run_number ...`

6. **Cache JAR file**
   - 📦 Action: `actions/cache@v3`
   - ⚙️ Config:
     - `path`: `build/libs/*.jar...`
     - `key`: `${{ steps.set-cache-key.outputs.cache-key }}...`

7. **Upload JAR as artifact**
   - 📦 Action: `actions/upload-artifact@v3`
   - ⚙️ Config:
     - `name`: `built-jar...`
     - `path`: `build/libs/*.jar...`

8. **List JAR files**
   - 💻 Run: `ls -l build/libs...`

---

*This documentation is auto-generated. Do not edit manually.*
