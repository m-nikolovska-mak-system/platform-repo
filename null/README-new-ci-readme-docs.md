# 📝 Auto-Generate Workflow Documentation

> **Type:** Manual Dispatch + Automated  
> **Source:** `new-ci-readme-docs.yml`

## 📋 Overview

This document provides comprehensive documentation for the `📝 Auto-Generate Workflow Documentation` workflow.

---

## 🎯 Triggers

- **`workflow_dispatch`**
- **`pull_request`**
  - Paths (includes): `.github/workflows/*.yml, .github/workflows/*.yaml`

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

### 🔧 `detect-changes`

**Runs on:** `ubuntu-latest`

| Step | Uses | Run |
| ---- | ---- | --- |
| Checkout | `actions/checkout@v4` | `` |
| Detect changed workflows | `tj-actions/changed-files@v44` | `` |
| Stop if no workflow changes |  | `echo "No workflow changes detected." && exit 0` |
| Prepare matrix JSON |  | ✅ Yes (see full YAML) |
| Get PR source branch |  | `echo "pr_source_branch=${{ github.head_ref }}" >> $GITHUB_OUTPUT` |

### 🔧 `update-doc`

**Runs on:** `ubuntu-latest`

| Step | Uses | Run |
| ---- | ---- | --- |
| Checkout | `actions/checkout@v4` | `` |
| Set up Python | `actions/setup-python@v5` | `` |
| Install dependencies |  | `pip install pyyaml` |
| Ensure docs directory exists |  | `mkdir -p docs` |
| Create missing README if needed |  | ✅ Yes (see full YAML) |
| Generate documentation (Python extractor) |  | ✅ Yes (see full YAML) |
| Verify README changed | `tj-actions/verify-changed-files@v19` | `` |
| Create Pull Request for Documentation Update | `peter-evans/create-pull-request@v6` | `` |


---

## 📄 Full Workflow YAML

<details>
<summary>Click to expand full YAML definition</summary>

```yaml
name: 📝 Auto-Generate Workflow Documentation

on:
  workflow_dispatch:
  pull_request:
    paths:
      - ".github/workflows/*.yml"
      - ".github/workflows/*.yaml"

permissions:
  contents: write
  pull-requests: write

env:
  GITHUB_USER_TOKEN: ${{ secrets.USER_TOKEN }}
  GITHUB_USER_EMAIL: "email@company.net"
  GITHUB_USER_NAME: "user1"

jobs:
  detect-changes:
    name: 🔍 Detect Changed Workflows
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.prep_matrix.outputs.matrix }}
      pr_source_branch: ${{ steps.get_source_branch.outputs.pr_source_branch }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Detect changed workflows
        id: detect
        uses: tj-actions/changed-files@v44
        with:
          files: |
            .github/workflows/*.yml
            .github/workflows/*.yaml
            !.github/workflows/ci-readme-docs.yml

      - name: Stop if no workflow changes
        if: steps.detect.outputs.any_changed == 'false'
        run: echo "No workflow changes detected." && exit 0

      - name: Prepare matrix JSON
        id: prep_matrix
        run: |
          json="[]"
          for f in ${{ steps.detect.outputs.all_changed_files }}; do
            base=$(basename "$f")
            base="${base%.yml}"
            base="${base%.yaml}"
            json=$(echo "$json" | jq --arg wf "$f" --arg b "$base" '. += [{"workflow":$wf,"basename":$b}]')
          done
          echo "matrix=$(echo "$json" | jq -c '.')" >> $GITHUB_OUTPUT

      - name: Get PR source branch
        id: get_source_branch
        run: echo "pr_source_branch=${{ github.head_ref }}" >> $GITHUB_OUTPUT

  update-doc:
    name: 📝 Generate & Update Workflow READMEs
    needs: detect-changes
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        item: ${{ fromJson(needs.detect-changes.outputs.matrix) }}

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ env.GITHUB_USER_TOKEN }}

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install pyyaml

      - name: Ensure docs directory exists
        run: mkdir -p docs

      # ------------------------------
      #   1. Create missing README from template
      # ------------------------------
      - name: Create missing README if needed
        id: create_readme
        run: |
          TEMPLATE="docs/README-reusable.md"
          README="docs/README-${{ matrix.item.basename }}.md"

          if [ ! -f "$README" ]; then
            echo "Creating missing README: $README"
            cp "$TEMPLATE" "$README"
            sed -i "/^## Usage$/a Documentation for workflow ${{ matrix.item.basename }}." "$README"
          fi

      # ------------------------------
      #   2. Run *your Python extractor*
      # ------------------------------
      - name: Generate documentation (Python extractor)
        run: |
          python3 scripts/extract-v2.py \
            "${{ matrix.item.workflow }}" \
            "docs/README-${{ matrix.item.basename }}.md"

      # ------------------------------
      #   3. Verify README changes
      # ------------------------------
      - name: Verify README changed
        id: verify
        uses: tj-actions/verify-changed-files@v19
        with:
          files: docs/README-${{ matrix.item.basename }}.md

      # ------------------------------
      #   4. Create PR (only if changed)
      # ------------------------------
      - name: Create Pull Request for Documentation Update
        if: steps.verify.outputs.files_changed == 'true'
        uses: peter-evans/create-pull-request@v6
        with:
          commit-message: "docs: auto-update README for ${{ matrix.item.basename }}"
          title: "docs: auto-update README for ${{ matrix.item.basename }}"
          body: |
            This PR updates the documentation for:
            **${{ matrix.item.basename }}**
          branch: "auto-doc/update-readme-${{ matrix.item.basename }}"
          committer: ${{ env.GITHUB_USER_NAME }} <${{ env.GITHUB_USER_EMAIL }}>
          token: ${{ env.GITHUB_USER_TOKEN }}
          base: ${{ needs.detect-changes.outputs.pr_source_branch || github.event.pull_request.base.ref }}
```

</details>

---

**Generated on:** 2025-12-01 09:33:25 UTC
