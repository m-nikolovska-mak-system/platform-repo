# Test – Mixed Triggers

> **Type:** Manual Dispatch + Automated  
> **Source:** `hellomultiple.yml`

## 📋 Overview

This document provides comprehensive documentation for the `Test – Mixed Triggers` workflow.

---

## 🎯 Triggers

- **`push`**
  - Branches: `main, dev`
- **`pull_request`**
  - Types: `opened, synchronize`
- **`workflow_dispatch`**


---

## 📥 Inputs

_This workflow does not accept any inputs._

---

## 📤 Outputs

_This workflow does not expose any outputs._

---

## 🔐 Secrets

_This workflow does not require any secrets._

---

## 💼 Jobs

### 🔧 `hello`

**Runs on:** `ubuntu-latest`

| Step | Uses | Run Command |
| ---- | ---- | ----------- |
| Step 1 |  | `echo "multi-trigger"` |



---

## 📄 Full Workflow YAML

<details>
<summary>Click to expand full YAML definition</summary>

```yaml
name: Test – Mixed Triggers
on:
  push:
    branches: ["main", "dev"]
  pull_request:
    types: ["opened", "synchronize"]
  workflow_dispatch:

jobs:
  hello:
    runs-on: ubuntu-latest
    steps:
      - run: echo "multi-trigger"
```

</details>

---

**Generated on:** 2025-11-28 15:29:02  
**Last Updated:** Check the workflow file history for the most recent changes.
