#!/usr/bin/env python3
import yaml
import argparse
from pathlib import Path
from datetime import datetime

# ------------------------------
# Helper functions
# ------------------------------
def generate_triggers(on):
    if isinstance(on, str):
        return f"- `{on}`"
    if isinstance(on, list):
        return "\n".join(f"- `{t}`" for t in on)
    if isinstance(on, dict):
        return "\n".join(f"- `{k}`" for k in on.keys())
    return "_No triggers defined._"

def generate_inputs(on):
    inputs = {}
    for key in ['workflow_call', 'workflow_dispatch']:
        if isinstance(on.get(key), dict):
            inputs.update(on[key].get('inputs', {}))
    
    if not inputs:
        return "_This workflow does not accept any inputs._"
    
    rows = ["| Name | Required | Description |", "| ---- | -------- | ----------- |"]
    for name, props in inputs.items():
        req = "✅" if props.get('required') else "❌"
        desc = props.get('description', '_No description provided_')
        rows.append(f"| `{name}` | {req} | {desc} |")
    return "\n".join(rows)

def generate_outputs(on):
    wf_call = on.get('workflow_call', {})
    outputs = wf_call.get('outputs', {}) if isinstance(wf_call, dict) else {}
    
    if not outputs:
        return "_This workflow does not expose any outputs._"
    
    rows = ["| Name | Description | Value |", "| ---- | ----------- | ----- |"]
    for name, props in outputs.items():
        desc = props.get('description', '_No description provided_')
        value = props.get('value', '_not specified_')
        rows.append(f"| `{name}` | {desc} | `{value}` |")
    return "\n".join(rows)

def generate_secrets(on):
    wf_call = on.get('workflow_call', {})
    secrets = wf_call.get('secrets', {}) if isinstance(wf_call, dict) else {}
    
    if not secrets:
        return "_This workflow does not require any secrets._"
    
    rows = ["| Name | Required | Description |", "| ---- | -------- | ----------- |"]
    for name, props in secrets.items():
        req = "✅" if props.get('required') else "❌"
        desc = props.get('description', '_No description provided_')
        rows.append(f"| `{name}` | {req} | {desc} |")
    return "\n".join(rows)

def generate_jobs(workflow):
    jobs = workflow.get('jobs', {})
    if not jobs:
        return "_No jobs defined._"
    
    sections = []
    for job_name, job in jobs.items():
        sections.append(f"### `{job_name}`")
        runs_on = job.get('runs-on', '')
        if runs_on:
            sections.append(f"**Runs on:** `{runs_on}`")
        
        steps = job.get('steps', [])
        if steps:
            rows = ["| Step | Uses | Run Command |", "| ---- | ---- | ----------- |"]
            for i, step in enumerate(steps, 1):
                name = step.get('name', f'Step {i}')
                uses = step.get('uses', '')
                run_cmd = step.get('run', '')
                
                # Handle run command display
                if run_cmd:
                    # Clean up multiline commands
                    run_display = ' '.join(run_cmd.strip().split())
                    if len(run_display) > 50:
                        run_display = "✅ Yes (see YAML)"
                    else:
                        # Escape pipes that break markdown tables
                        run_display = run_display.replace('|', '\\|')
                        run_display = f"`{run_display}`"
                else:
                    run_display = ''
                
                uses_display = f"`{uses}`" if uses else ''
                rows.append(f"| {name} | {uses_display} | {run_display} |")
            sections.append("\n".join(rows))
    
    return "\n\n".join(sections)

# ------------------------------
# Main function
# ------------------------------
def generate_doc(yaml_file):
    """Generate documentation from workflow YAML file"""
    try:
        workflow = yaml.safe_load(Path(yaml_file).read_text(encoding='utf-8'))
    except Exception as e:
        print(f"❌ Error parsing YAML: {e}")
        return None
    
    name = workflow.get('name', 'Unnamed Workflow')
    on = workflow.get('on', {})
    
    # Read the full YAML for embedding
    full_yaml = Path(yaml_file).read_text(encoding='utf-8').rstrip()
    
    doc = f"""# {name}

## 📋 Overview

This document provides comprehensive documentation for the **{name}** workflow.

---

## 🎯 Triggers

{generate_triggers(on)}

---

## 📥 Inputs

{generate_inputs(on)}

---

## 📤 Outputs

{generate_outputs(on)}

---

## 🔐 Secrets

{generate_secrets(on)}

---

## 💼 Jobs

{generate_jobs(workflow)}

---

## 📄 Full Workflow YAML

<details>
<summary>Click to expand full YAML definition</summary>

```yaml
{full_yaml}
```

</details>

---

**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    return doc

# ------------------------------
# Command-line interface
# ------------------------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate workflow documentation'
    )
    parser.add_argument('--workflow', required=True, help='Path to workflow YAML file')
    parser.add_argument('--output', required=True, help='Path to output README file')
    parser.add_argument('--template', help='Path to template file (not used in this version)')
    
    args = parser.parse_args()
    
    # Generate documentation
    doc_content = generate_doc(args.workflow)
    
    if doc_content is None:
        print("❌ Failed to generate documentation")
        exit(1)
    
    # Ensure output directory exists
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write output
    try:
        output_path.write_text(doc_content, encoding='utf-8')
        print(f"✅ Generated documentation: {args.output}")
    except Exception as e:
        print(f"❌ Error writing output file: {e}")
        exit(1)
