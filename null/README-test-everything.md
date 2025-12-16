# Everything Workflow

> **Type:** Reusable Workflow + Manual Dispatch + Automated  
> **Source:** `test-everything.yml`

## 📋 Overview

This document provides comprehensive documentation for the `Everything Workflow` workflow.

---

## 🎯 Triggers

- **`push`**
  - Branches: `main`
- **`release`**
  - Types: `published`
- **`workflow_dispatch`**
- **`workflow_call`**

---

## 📥 Inputs

| Name | Type | Required | Default | Description |
| ---- | ---- | -------- | ------- | ----------- |
| `caller_input` | `string` | ❌ No | `_not set_` | _No description provided_ |
| `mode` | `string` | ❌ No | `default` | _No description provided_ |

---

## 📤 Outputs

| Name | Description | Value |
| ---- | ----------- | ----- |
| `final_message` | A message returned from the workflow | `${{ jobs.run.outputs.message }}` |
| `build_artifact` | Where an artifact ended up | `${{ jobs.run.outputs.artifact_path }}` |

---

## 🔐 Secrets

| Name | Required | Description |
| ---- | -------- | ----------- |
| `CALLER_SECRET` | ❌ No | _No description provided_ |

---

## 💼 Jobs

### 🔧 `run`

**Runs on:** `ubuntu-latest`

| Step | Uses | Run |
| ---- | ---- | --- |
| Create message output |  | `echo "msg=Hello from Everything Workflow!" >> $GITHUB_OUTPUT` |
| Create fake artifact path |  | `echo "path=/tmp/build/output.zip" >> $GITHUB_OUTPUT` |
| Indicator |  | `echo "Running everything workflow"` |


---

## 📄 Full Workflow YAML

<details>
<summary>Click to expand full YAML definition</summary>

```yaml
name: Everything Workflow

on:
  push:
    branches: [main]
  release:
    types: [published]
  workflow_dispatch:
    inputs:
      mode:
        type: string
        required: false
        default: "default"
  workflow_call:
    inputs:
      caller_input:
        type: string
        required: false
    secrets:
      CALLER_SECRET:
        required: false
    outputs:
      final_message:
        description: "A message returned from the workflow"
        value: ${{ jobs.run.outputs.message }}
      build_artifact:
        description: "Where an artifact ended up"
        value: ${{ jobs.run.outputs.artifact_path }}

jobs:
  run:
    runs-on: ubuntu-latest
    outputs:
      message: ${{ steps.create_msg.outputs.msg }}
      artifact_path: ${{ steps.artifact.outputs.path }}

    steps:
      - name: Create message output
        id: create_msg
        run: |
          echo "msg=Hello from Everything Workflow!" >> $GITHUB_OUTPUT

      - name: Create fake artifact path
        id: artifact
        run: |
          echo "path=/tmp/build/output.zip" >> $GITHUB_OUTPUT

      - name: Indicator
        run: echo "Running everything workflow"
```

</details>

---

**Generated on:** 2025-12-01 09:47:05 UTC
