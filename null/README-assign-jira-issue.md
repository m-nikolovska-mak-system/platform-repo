# Assign Jira Issue ng this! again hi testing hi

> **Type:** Manual Dispatch  
> **Source:** `assign-jira-issue.yml`

## 📋 Overview

This document provides comprehensive documentation for the `Assign Jira Issue ng this! again hi testing hi` workflow.

---

## 🎯 Triggers

- **`workflow_dispatch`**

---

## 📥 Inputs

| Name | Type | Required | Default | Description |
| ---- | ---- | -------- | ------- | ----------- |
| `issue_key` | `string` | ✅ Yes | `_not set_` | Jira issue key (e.g. ABC-123) |
| `assignee_email` | `string` | ✅ Yes | `_not set_` | Assignee email in Jira |

---

## 📤 Outputs

_This workflow does not expose any outputs._

---

## 🔐 Secrets

_This workflow does not require any secrets._

---

## 💼 Jobs

### 🔧 `assign`

**Runs on:** `ubuntu-latest`

| Step | Uses | Run |
| ---- | ---- | --- |
| Install jq and python3 |  | `sudo apt-get update -y sudo apt-get install -y jq python3` |
| Assign issue in Jira |  | ✅ Yes (see full YAML) |


---

## 📄 Full Workflow YAML

<details>
<summary>Click to expand full YAML definition</summary>

```yaml
name: Assign Jira Issue ng this! again hi testing hi
on:
  workflow_dispatch:
    inputs:
      issue_key:
        description: 'Jira issue key (e.g. ABC-123)'
        required: true
      assignee_email:
        description: 'Assignee email in Jira'
        required: true

jobs:
  assign:
    runs-on: ubuntu-latest
    steps:
      - name: Install jq and python3
        run: |
          sudo apt-get update -y
          sudo apt-get install -y jq python3

      - name: Assign issue in Jira
        env:
          JIRA_EMAIL: ${{ secrets.JIRA_USER }}
          JIRA_API_TOKEN: ${{ secrets.JIRA_API_TOKEN }}
          JIRA_URL: ${{ secrets.JIRA_BASE_URL }}
          ISSUE_KEY: ${{ github.event.inputs.issue_key }}
          ASSIGNEE_EMAIL: ${{ github.event.inputs.assignee_email }}
        run: |
          set -e
          if [ -z "$JIRA_EMAIL" ] || [ -z "$JIRA_API_TOKEN" ] || [ -z "$JIRA_URL" ]; then
            echo "Missing Jira secrets: JIRA_EMAIL, JIRA_API_TOKEN, JIRA_URL"
            exit 1
          fi

          echo "Looking up Jira user by email: $ASSIGNEE_EMAIL"
          QUERY_ENC=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$ASSIGNEE_EMAIL")
          SEARCH_JSON=$(curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" "$JIRA_URL/rest/api/3/user/search?query=$QUERY_ENC")
          ACCOUNT_ID=$(echo "$SEARCH_JSON" | jq -r '.[0].accountId // empty') || true

          if [ -z "$ACCOUNT_ID" ]; then
            echo "Could not find Jira user for email: $ASSIGNEE_EMAIL"
            echo "Search response: $SEARCH_JSON"
            exit 1
          fi

          echo "Found accountId: $ACCOUNT_ID"
          PAYLOAD=$(jq -n --arg acc "$ACCOUNT_ID" '{accountId: $acc}')

          echo "Assigning issue $ISSUE_KEY to $ASSIGNEE_EMAIL (accountId: $ACCOUNT_ID)"
          RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -u "$JIRA_EMAIL:$JIRA_API_TOKEN" -X PUT -H "Content-Type: application/json" --data "$PAYLOAD" "$JIRA_URL/rest/api/3/issue/$ISSUE_KEY/assignee")
          echo "Assign HTTP response: $RESPONSE"

          if [ "$RESPONSE" -ne 204 ]; then
            echo "Failed to assign issue. HTTP code: $RESPONSE"
            exit 1
          fi

          echo "Issue $ISSUE_KEY assigned to $ASSIGNEE_EMAIL"
```

</details>

---

**Generated on:** 2025-12-03 14:48:25 UTC
