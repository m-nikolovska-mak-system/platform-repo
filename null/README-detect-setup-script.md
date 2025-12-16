# 📝 Detect Setup Script

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Detect Setup Script`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `detect-iss`

**Runner:** `ubuntu-latest`

**Job Outputs:**

- `setup_script`: `${{ steps.detect.outputs.script }}`

**Steps:**

1. **Checkout code**
   - 📦 Action: `actions/checkout@v4`

2. **Detect .iss setup script**
   - 💻 Run: `file=$(ls *.iss 2>/dev/null | head -n 1)...`

---

*This documentation is auto-generated. Do not edit manually.*
