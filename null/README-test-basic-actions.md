# 📝 Test Basic Actions (Optimized)

**Generated:** 2025-11-26 12:28:06

---

## Overview

**Workflow Name:** `Test Basic Actions (Optimized)`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `validate_readme`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Sparse checkout (README only!)**
   - 📦 Action: `actions/checkout@v4`
   - ⚙️ Config:
     - `sparse-checkout`: `README.md ...`
     - `sparse-checkout-cone-mode`: `False...`

2. **Run README Validator**
   - 📦 Action: `./.github/actions/readme-validator`
   - ⚙️ Config:
     - `min_lines`: `5...`

### `lint_check`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Sparse checkout (only what we need to lint)**
   - 📦 Action: `actions/checkout@v4`
   - ⚙️ Config:
     - `sparse-checkout`: `src/ scripts/ .github/actions/lint-check/ ...`
     - `sparse-checkout-cone-mode`: `False...`

2. **Run Linting Check**
   - 📦 Action: `./.github/actions/lint-check`
   - ⚙️ Config:
     - `file`: `....`

---

*This documentation is auto-generated. Do not edit manually.*
