# 📝 📝 Generate/Update README Documentation

**Generated:** 2025-11-26 12:28:06

---

## Overview

**Workflow Name:** `📝 Generate/Update README Documentation`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `detect-changes`

**Runner:** `ubuntu-latest`

**Job Outputs:**

- `matrix`: `${{ steps.prep_matrix.outputs.matrix }}`
- `pr_source_branch`: `${{ steps.get_source_branch.outputs.pr_source_branch }}`
- `has_changes`: `${{ steps.detect.outputs.any_changed }}`

**Steps:**

1. **Checkout**
   - 📦 Action: `actions/checkout@v4`

2. **Detect changed workflow files**
   - 📦 Action: `tj-actions/changed-files@v44`
   - ⚙️ Config:
     - `files`: `.github/workflows/ci-*.yml !.github/workflows/gene...`

3. **Print changed workflow files**
   - 💻 Run: `echo "Changed workflow files:"...`

4. **Stop if no workflows changed**
   - 💻 Run: `echo "No workflow changes detected. Skipping documentation."...`

5. **Prepare matrix JSON**
   - 💻 Run: `json="[]"...`

6. **Get PR source branch**
   - 💻 Run: `echo "pr_source_branch=${{ github.head_ref }}" >> $GITHUB_OU...`

### `update-doc`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Checkout**
   - 📦 Action: `actions/checkout@v4`
   - ⚙️ Config:
     - `fetch-depth`: `0...`
     - `token`: `${{ secrets.USER_TOKEN }}...`

2. **Create missing READMEs**
   - 💻 Run: `TEMPLATE="docs/README-reusable.md"...`

3. **Print newly created README files**
   - 💻 Run: `if [ -n "${{ steps.create_readmes.outputs.new_readmes }}" ];...`

4. **Print workflow file from matrix**
   - 💻 Run: `echo "Current workflow file: ${{ matrix.item.workflow }}"...`

5. **Auto-doc for workflow**
   - 📦 Action: `tj-actions/auto-doc@v3`
   - ⚙️ Config:
     - `filename`: `./${{ matrix.item.workflow }}...`
     - `reusable`: `True...`
     - `output`: `docs/README-${{ matrix.item.basename }}.md...`

6. **Verify changed README**
   - 📦 Action: `tj-actions/verify-changed-files@v19`
   - ⚙️ Config:
     - `files`: `docs/README-${{ matrix.item.basename }}.md...`

7. **Print verification result**
   - 💻 Run: `if [ "${{ steps.verify.outputs.files_changed }}" == "true" ]...`

8. **Print target branch**
   - 💻 Run: `echo "*** branch *** " ${{ needs.detect-changes.outputs.pr_s...`

9. **Create Pull Request for Documentation Update**
   - 📦 Action: `peter-evans/create-pull-request@v6`
   - ⚙️ Config:
     - `commit-message`: `docs: auto-update README for ${{ matrix.item.basen...`
     - `title`: `docs: auto-update README for ${{ matrix.item.basen...`
     - `body`: `This PR was automatically generated to update the ...`

---

*This documentation is auto-generated. Do not edit manually.*
