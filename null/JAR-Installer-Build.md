# 🔄 Automated Build & Release Workflows (Java JAR + Windows Installer)

This repository includes **two GitHub Actions workflows** that automate:

- ✅ Building a Java JAR file using Gradle  
- ✅ Creating a Windows installer (`.exe`) using Inno Setup  
- ✅ Uploading the installer to a GitHub Release  

The system is designed to be **reusable, robust, and cache-friendly**, suitable for enterprise projects.

---

## 📂 Workflow Files

### 1. **Main Build and Release**  
File: `.github/workflows/main-build.yml`  

**Purpose:**  

- Triggered automatically on **GitHub Release creation** or manually via Actions → Run workflow.  
- Builds the JAR with Gradle.  
- Caches the JAR for reuse across workflow runs.  
- Calls the reusable **Build Installer** workflow.  
- Uploads the final `.exe` installer to the Release page.

---

### 2. **Build Installer (Reusable)**  
File: `.github/workflows/build-installer.yml`  

**Purpose:**  

- Builds the Windows installer using **Inno Setup**.  
- Accepts inputs such as JAR cache key, release tag, app name, app version, and setup script.  
- Designed as a **reusable workflow** that can be called from multiple repositories or workflows.  
- Uploads the installer as a workflow artifact for consumption by the calling workflow.

---

## ✅ How It Works (Step-by-Step)

1. **Developer creates a GitHub Release** (or triggers manually).  
2. `main-build.yml` runs:  
   - Checks out the code.  
   - Builds the JAR with Gradle.  
   - Caches the JAR for future runs.  
   - Calls `build-installer.yml` and passes the cache key.  
3. `build-installer.yml` runs:  
   - Restores the cached JAR.  
   - Installs Inno Setup via Chocolatey.  
   - Dynamically detects the `.iss` setup script.  
   - Compiles the installer using `ISCC.exe` with parameters:  
     - `/DAppName=<App Name>`  
     - `/DAppVersion=<App Version>`  
     - `/DJarFileName=<JAR Filename>`  
     - `/DOutputBaseName=<Installer Name>`  
   - Uploads the installer as a workflow artifact.  
4. Back in `main-build.yml`:  
   - Downloads the installer artifact.  
   - Uploads it to the GitHub Release.

---

## 🔧 Setup and Usage

### **1. Copy the workflows**

- Place both workflow files in `.github/workflows/` in your repository.

### **2. Update Inno Setup script (`.iss`)**

- Create or modify a setup script in your repo (`setup-script.iss`). Example parameters handled by the workflow:

```iss
#ifndef AppName
  #define AppName "DefaultApp"
#endif
#ifndef AppVersion
  #define AppVersion "1.0.0"
#endif
#ifndef JarFileName
  #define JarFileName "app.jar"
#endif
#ifndef OutputBaseName
  #define OutputBaseName "Setup"
#endif

[Setup]
AppName={#AppName}
AppVersion={#AppVersion}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
OutputDir=output
OutputBaseFilename={#OutputBaseName}
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=lowest

[Files]
Source: "build\libs\{#JarFileName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#AppName}"; Filename: "javaw.exe"; Parameters: "-jar ""{app}\{#JarFileName}"""; WorkingDir: "{app}"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"
