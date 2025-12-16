# Build JAR this is a duplicate with a differenect name to HELLOO aaaaaaaaaaa testing 22aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaahhhhhhaaaaaa hi testing hello hello again once more a testaaaaaaaaaaaaaaaaaaaa

> **Type:** Reusable Workflow  
> **Source:** `ci-build-jar.yml`

## 📋 Overview

This document provides comprehensive documentation for the `Build JAR this is a duplicate with a differenect name to HELLOO aaaaaaaaaaa testing 22aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaahhhhhhaaaaaa hi testing hello hello again once more a testaaaaaaaaaaaaaaaaaaaa` workflow.

---

## 🎯 Triggers

- **`workflow_call`**

---

## 📥 Inputs

| Name | Type | Required | Default | Description |
| ---- | ---- | -------- | ------- | ----------- |
| `release_tag` | `string` | ❌ No | `main` | _No description provided_ |
| `gradle_task` | `string` | ❌ No | `jar` | _No description provided_ |
| `gradle_task_two0aao` | `string` | ❌ No | `jar3` | _No description provided_ |


---

## 📤 Outputs

| Name | Description | Value |
| ---- | ----------- | ----- |
| `jar_cache_key` | Cache key for restored JAR | `${{ jobs.build-jar.outputs.jar_cache_key }}` |


---

## 🔐 Secrets

| Name | Required | Description |
| ---- | -------- | ----------- |
| `TEST_SECRET` | ✅ Yes | _No description provided_ |


---

## 💼 Jobs

### 🔧 `build-jar`

**Runs on:** `ubuntu-latest`

| Step | Uses | Run Command |
| ---- | ---- | ----------- |
| Checkout code | `actions/checkout@v4` |  |
| Set up Java 17 | `actions/setup-java@v3` |  |
| Make Gradle wrapper executable |  | `chmod +x gradlew` |
| Cache Gradle dependencies | `actions/cache@v3` |  |
| Build JAR |  | `./gradlew ${{ inputs.gradle_task }} --no-daemon` |
| Validate JAR |  | ✅ Yes (see YAML) |
| Generate cache key |  | ✅ Yes (see YAML) |
| Cache built JAR | `actions/cache/save@v3` |  |



---

## 📄 Full Workflow YAML

<details>
<summary>Click to expand full YAML definition</summary>

```yaml
name: Build JAR this is a duplicate with a differenect name to HELLOO aaaaaaaaaaa testing 22aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaahhhhhhaaaaaa hi testing hello hello again once more a testaaaaaaaaaaaaaaaaaaaa

on:
  workflow_call:
    inputs:
      release_tag:
        required: false
        type: string
        default: "main"
      gradle_task:
        required: false
        type: string
        default: "jar"
      gradle_task_two0aao:
        required: false
        type: string
        default: "jar3"
    outputs:
      jar_cache_key:
        description: "Cache key for restored JAR"
        value: ${{ jobs.build-jar.outputs.jar_cache_key }}
    secrets:
      TEST_SECRET:
        required: true

      

jobs:
  build-jar:
    runs-on: ubuntu-latest
    outputs:
      jar_cache_key: ${{ steps.cache-key.outputs.key }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          ref: ${{ inputs.release_tag }}

      - name: Set up Java 17
        uses: actions/setup-java@v3
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Make Gradle wrapper executable
        run: chmod +x gradlew

      - name: Cache Gradle dependencies
        uses: actions/cache@v3
        with:
          path: |
            ~/.gradle/caches
            ~/.gradle/wrapper
          key: ${{ runner.os }}-gradle-${{ hashFiles('**/*.gradle*', '**/gradle-wrapper.properties') }}
          restore-keys: |
            ${{ runner.os }}-gradle-

      - name: Build JAR
        run: ./gradlew ${{ inputs.gradle_task }} --no-daemon

      - name: Validate JAR
        run: |
          jar_file=$(ls build/libs/*.jar 2>/dev/null | head -n 1)
          if [ -z "$jar_file" ]; then
            echo "❌ No JAR files found"
            exit 1
          fi
          echo "✓ Found $(basename "$jar_file")"

      - name: Generate cache key
        id: cache-key
        run: echo "key=jar-${{ github.sha }}-${{ github.run_number }}" >> $GITHUB_OUTPUT

      - name: Cache built JAR
        uses: actions/cache/save@v3
        with:
          path: build/libs/*.jar
          key: ${{ steps.cache-key.outputs.key }}
```

</details>

---

**Generated on:** 2025-11-28 15:11:34  
**Last Updated:** Check the workflow file history for the most recent changes.
