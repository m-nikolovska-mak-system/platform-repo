# 🚀 GitHub Actions CI/CD for Java App + Inno Setup Installer

This repository uses **GitHub Actions reusable workflows** to build a Java application, detect an Inno Setup script, create a Windows installer, and publish it to a GitHub Release.

---

## ✅ Overview of Workflow Architecture

**Main Workflow:** `main-build-and-release.yml`  

- **Trigger:** Runs when a new GitHub Release is created  
- **Purpose:** Orchestrates the entire build and release process by calling reusable workflows  

**Jobs:**
1. `build_jar` → Builds the JAR file and outputs a cache key  
2. `detect_iss` → Detects `.iss` setup script for Inno Setup  
3. `build_installer` → Creates a Windows installer using Inno Setup  
4. `upload_release` → Downloads the installer artifact and attaches it to the GitHub Release  

---

## ✅ Reusable Workflows

### `build-jar.yml`
- Builds the Java JAR using Gradle  
- Outputs `jar_cache_key` for caching  

---

### `detect-setup-script.yml`
- Detects `.iss` setup script in the repo  
- Outputs `setup_script` for installer build  

---

### `build-installer.yml`
- Runs on `windows-latest`  
- Installs Inno Setup via Chocolatey  
- Builds the installer `.exe` using the detected script  
- Uploads the installer as an artifact (`setup-installer`)  
- Outputs `installer_file` (full path to `.exe`)  

---

### `upload-release.yml`
- Downloads the installer artifact  
- Verifies the file exists  
- Uploads the `.exe` to the GitHub Release using `softprops/action-gh-release`  

---

## ✅ Main Workflow Example

```yaml
name: Main Build and Release

on:
  release:
    types: [created]

jobs:
  build_jar:
    uses: ./.github/workflows/build-jar.yml
    with:
      release_tag: ${{ github.event.release.tag_name }}

  detect_iss:
    uses: ./.github/workflows/detect-setup-script.yml

  build_installer:
    needs: [build_jar, detect_iss]
    uses: ./.github/workflows/build-installer.yml
    with:
      jar_cache_key: ${{ needs.build_jar.outputs.jar_cache_key }}
      release_tag: ${{ github.event.release.tag_name }}
      setup_script: ${{ needs.detect_iss.outputs.setup_script }}
      app_name: ${{ github.event.repository.name }}
      app_version: ${{ github.event.release.tag_name }}
      output_name: "Setup-${{ github.event.release.tag_name }}"

  upload_release:
    needs: build_installer
    uses: ./.github/workflows/upload-release.yml
    with:
      artifact_path: ${{ needs.build_installer.outputs.installer_file }}
      tag_name: ${{ github.event.release.tag_name }}
