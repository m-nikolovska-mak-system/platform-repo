# 📝 📝 Auto-generate workflow READMEs v5

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `📝 Auto-generate workflow READMEs v5`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `detect-changes`

**Runner:** `ubuntu-latest`

**Job Outputs:**

- `matrix`: `${{ steps.handle_matrix.outputs.matrix }}`
- `has_changes`: `${{ steps.handle_matrix.outputs.has_changes }}`
- `pr_source_branch`: `${{ steps.get_source_branch.outputs.pr_source_branch }}`

**Steps:**

1. **Checkout**
   - 📦 Action: `actions/checkout@v4`
   - ⚙️ Config:
     - `fetch-depth`: `0...`
     - `token`: `${{ secrets.GITHUB_TOKEN }}...`

2. **Detect changed workflow files**
   - 📦 Action: `tj-actions/changed-files@v44`
   - ⚙️ Config:
     - `files`: `.github/workflows/*.yml !.github/workflows/workflo...`

3. **Prepare matrix**
   - 💻 Run: `files="${{ steps.detect.outputs.all_changed_files }}"...`

4. **Handle empty matrix**
   - 💻 Run: `if [ "${{ steps.detect.outputs.any_changed }}" = "false" ]; ...`

5. **Get PR source branch**
   - 💻 Run: `echo "pr_source_branch=${{ github.head_ref || github.ref_nam...`

### `update-doc`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Checkout**
   - 📦 Action: `actions/checkout@v4`
   - ⚙️ Config:
     - `fetch-depth`: `0...`
     - `token`: `${{ secrets.GITHUB_TOKEN }}...`

2. **Ensure docs folder**
   - 💻 Run: `mkdir -p docs...`

3. **Auto-doc for workflow**
   - 📦 Action: `tj-actions/auto-doc@v3`
   - ⚙️ Config:
     - `filename`: `./${{ matrix.workflow }}...`
     - `reusable`: `True...`
     - `output`: `docs/README-${{ matrix.basename }}.md...`

4. **Verify changed README**
   - 📦 Action: `tj-actions/verify-changed-files@v19`
   - ⚙️ Config:
     - `files`: `docs/README-${{ matrix.basename }}.md...`

5. **Create Pull Request for Documentation Update**
   - 📦 Action: `peter-evans/create-pull-request@v6`
   - ⚙️ Config:
     - `commit-message`: `docs: auto-update README for ${{ matrix.basename }...`
     - `title`: `docs: auto-update README for ${{ matrix.basename }...`
     - `body`: `This PR auto-updates the documentation for workflo...`

---

*This documentation is auto-generated. Do not edit manually.*
