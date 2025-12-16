# 📝 Test Composite Action

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Test Composite Action`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `test-readme-validator`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Step 1**
   - 📦 Action: `actions/checkout@v3`

2. **Run README Validator**
   - 📦 Action: `./actions/readme-validator`
   - ⚙️ Config:
     - `input_file`: `README.md...`

---

*This documentation is auto-generated. Do not edit manually.*
