# 📝 Create Jira Task on Release

**Generated:** 2025-11-26 12:28:07

---

## Overview

**Workflow Name:** `Create Jira Task on Release`

## Triggers

*No triggers defined*

## 🔨 Jobs

### `create-jira-task`

**Runner:** `ubuntu-latest`

**Steps:**

1. **Checkout repository**
   - 📦 Action: `actions/checkout@v4`

2. **Create Jira task**
   - 📦 Action: `atlassian/gajira-create@v3`
   - ⚙️ Config:
     - `project`: `DEMO...`
     - `issuetype`: `Task...`
     - `summary`: `Prepare new installer for App.java changes...`

---

*This documentation is auto-generated. Do not edit manually.*
