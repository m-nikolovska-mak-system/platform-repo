# 📝 Build Windows Installer

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Build Windows Installer`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `build-installer`

**Runner:** `windows-latest`

**Steps:**

1. **Checkout repo**
   - 📦 Action: `actions/checkout@v4`
   - ⚙️ Config:
     - `ref`: `${{ github.event.inputs.release_tag }}...`

2. **Download built JAR from previous workflow**
   - 📦 Action: `actions/download-artifact@v4`
   - ⚙️ Config:
     - `name`: `app-jar...`
     - `path`: `build/libs...`

3. **Verify JAR**
   - 💻 Run: `dir build\libs...`

4. **Install Inno Setup**
   - 💻 Run: `choco install innosetup --no-progress -y...`

5. **Build setup.exe**
   - 💻 Run: `"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" .github\setup...`

6. **Upload setup.exe as artifact**
   - 📦 Action: `actions/upload-artifact@v4`
   - ⚙️ Config:
     - `name`: `setup-installer...`
     - `path`: `output/OneProjectWed-Setup.exe...`

7. **Check output folder**
   - 💻 Run: `dir output...`

8. **Upload setup.exe to GitHub Release**
   - 📦 Action: `softprops/action-gh-release@v2`
   - ⚙️ Config:
     - `files`: `output/OneProjectWed-Setup.exe...`
     - `tag_name`: `${{ github.event.inputs.release_tag }}...`

---

*This documentation is auto-generated. Do not edit manually.*
