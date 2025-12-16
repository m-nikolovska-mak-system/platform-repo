# 📝 Generate README

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Generate README`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `generate-readme`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Step 1**
   - 📦 Action: `actions/checkout@v3`

2. **Generate README**
   - 📦 Action: `bitflight-devops/github-action-readme-generator@v1`
   - ⚙️ Config:
     - `action`: `.github/workflows/hello.yml...`
     - `readme`: `AUTO_README.md...`
     - `save`: `False...`

---

*This documentation is auto-generated. Do not edit manually.*
