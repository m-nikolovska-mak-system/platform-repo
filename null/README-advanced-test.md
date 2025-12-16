# 📝 Advanced ACT Test

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Advanced ACT Test`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `test-matrix`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Setup Node.js ${{ matrix.node }}**
   - 📦 Action: `actions/setup-node@v3`
   - ⚙️ Config:
     - `node-version`: `${{ matrix.node }}...`

2. **Print Environment**
   - 💻 Run: `echo "Running on ${{ matrix.os }} with Node.js ${{ matrix.no...`

### `validate-inputs`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Check dry-run input**
   - 💻 Run: `if [[ "${{ github.event.inputs.dry_run }}" == "true" ]]; the...`

### `use-secrets`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Print secret (simulated)**
   - 💻 Run: `echo "Secret is set (not printing for safety)"...`

### `conditional-step`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Run only in dev**
   - 💻 Run: `echo "Running in development environment"...`

### `concurrency-test`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Simulate long task**
   - 💻 Run: `sleep 10...`

### `post-run-cleanup`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Setup**
   - 💻 Run: `echo "Setting up resources"...`

2. **Cleanup**
   - 💻 Run: `echo "Cleaning up resources"...`

---

*This documentation is auto-generated. Do not edit manually.*
