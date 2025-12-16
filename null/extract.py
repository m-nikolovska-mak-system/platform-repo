#!/usr/bin/env python3
import yaml
import sys
from datetime import datetime
from pathlib import Path

def main():
    # Get arguments
    workflow_file = sys.argv[1]
    output_file = sys.argv[2]
    
    print(f"📖 Reading: {workflow_file}")
    
    # Load YAML
    with open(workflow_file, 'r') as f:
        workflow = yaml.safe_load(f)
    
    # Get workflow name
    workflow_name = workflow.get('name', 'Unnamed Workflow')
    print(f"✅ Workflow: {workflow_name}")
    
    # Try to find 'on' key - it might be parsed as boolean True!
    on_key = None
    if 'on' in workflow:
        on_key = 'on'
    elif True in workflow:
        on_key = True
        print("🔍 Note: 'on' key parsed as boolean True (YAML quirk)")
    else:
        print("❌ Could not find 'on' key in workflow!")
        sys.exit(1)
    
    on_section = workflow.get(on_key, {})
    
    # ========== EXTRACT TRIGGERS ==========
    triggers = list(on_section.keys()) if isinstance(on_section, dict) else []
    print(f"✅ Triggers: {triggers}")
    
    # ========== EXTRACT INPUTS ==========
    inputs = {}
    if 'workflow_call' in on_section:
        wf_call = on_section['workflow_call']
        if wf_call and isinstance(wf_call, dict):
            inputs.update(wf_call.get('inputs', {}))
    
    if 'workflow_dispatch' in on_section:
        wf_dispatch = on_section['workflow_dispatch']
        if wf_dispatch and isinstance(wf_dispatch, dict):
            inputs.update(wf_dispatch.get('inputs', {}))
    
    print(f"✅ Inputs: {list(inputs.keys())}")
    
    # ========== EXTRACT OUTPUTS ==========
    outputs = {}
    if 'workflow_call' in on_section:
        wf_call = on_section['workflow_call']
        if wf_call and isinstance(wf_call, dict):
            outputs = wf_call.get('outputs', {})
    
    print(f"✅ Outputs: {list(outputs.keys())}")
    
    # ========== EXTRACT SECRETS ==========
    secrets = {}
    if 'workflow_call' in on_section:
        wf_call = on_section['workflow_call']
        if wf_call and isinstance(wf_call, dict):
            secrets = wf_call.get('secrets', {})
    
    print(f"✅ Secrets: {list(secrets.keys())}")
    
    # ========== EXTRACT JOBS ==========
    jobs = workflow.get('jobs', {})
    print(f"✅ Jobs: {list(jobs.keys())}")
    
    # ========== DETERMINE WORKFLOW TYPE ==========
    workflow_types = []
    if 'workflow_call' in triggers:
        workflow_types.append('Reusable Workflow')
    if 'workflow_dispatch' in triggers:
        workflow_types.append('Manual Dispatch')
    if any(t in triggers for t in ['push', 'pull_request', 'schedule', 'release']):
        workflow_types.append('Automated')
    
    workflow_type = ' + '.join(workflow_types) if workflow_types else 'Standard Workflow'
    
    # ========== FORMAT TRIGGERS ==========
    if triggers:
        triggers_text = ""
        for trigger in triggers:
            triggers_text += f"- **`{trigger}`**\n"
            
            # Add details for specific triggers
            trigger_config = on_section.get(trigger, {})
            if trigger_config and isinstance(trigger_config, dict):
                # Handle push/pull_request branches
                if 'branches' in trigger_config:
                    branches = trigger_config['branches']
                    if isinstance(branches, list):
                        triggers_text += f"  - Branches: `{', '.join(branches)}`\n"
                    else:
                        triggers_text += f"  - Branches: `{branches}`\n"
                
                # Handle paths
                if 'paths' in trigger_config:
                    paths = trigger_config['paths']
                    if isinstance(paths, list):
                        includes = [p for p in paths if not p.startswith('!')]
                        excludes = [p[1:] for p in paths if p.startswith('!')]
                        if includes:
                            triggers_text += f"  - Paths (includes): `{', '.join(includes)}`\n"
                        if excludes:
                            triggers_text += f"  - Paths (excludes): `{', '.join(excludes)}`\n"
                    else:
                        triggers_text += f"  - Paths: `{paths}`\n"
                
                # Handle types (for pull_request)
                if 'types' in trigger_config:
                    types = trigger_config['types']
                    if isinstance(types, list):
                        triggers_text += f"  - Types: `{', '.join(types)}`\n"
                    else:
                        triggers_text += f"  - Types: `{types}`\n"
                
                # Handle schedule (cron)
                if trigger == 'schedule' and isinstance(trigger_config, list):
                    triggers_text += f"  - Cron schedules:\n"
                    for schedule in trigger_config:
                        if 'cron' in schedule:
                            triggers_text += f"    - `{schedule['cron']}`\n"
    else:
        triggers_text = '_No triggers defined._'
    
    # ========== FORMAT INPUTS ==========
    if inputs:
        inputs_text = "| Name | Type | Required | Default | Description |\n"
        inputs_text += "| ---- | ---- | -------- | ------- | ----------- |\n"
        for name, props in inputs.items():
            inp_type = props.get('type', 'string')
            required = '✅ Yes' if props.get('required', False) else '❌ No'
            default = props.get('default', '_not set_')
            desc = props.get('description', '_No description provided_')
            inputs_text += f"| `{name}` | `{inp_type}` | {required} | `{default}` | {desc} |\n"
    else:
        inputs_text = "_This workflow does not accept any inputs._"
    
    # ========== FORMAT OUTPUTS ==========
    if outputs:
        outputs_text = "| Name | Description | Value |\n"
        outputs_text += "| ---- | ----------- | ----- |\n"
        for name, props in outputs.items():
            desc = props.get('description', '_No description provided_')
            value = props.get('value', '_not specified_')
            # Truncate long values
            if len(str(value)) > 60:
                value = f"{str(value)[:57]}..."
            outputs_text += f"| `{name}` | {desc} | `{value}` |\n"
    else:
        outputs_text = "_This workflow does not expose any outputs._"
    
    # ========== FORMAT SECRETS ==========
    if secrets:
        secrets_text = "| Name | Required | Description |\n"
        secrets_text += "| ---- | -------- | ----------- |\n"
        for name, props in secrets.items():
            required = '✅ Yes' if props.get('required', False) else '❌ No'
            desc = props.get('description', '_No description provided_')
            secrets_text += f"| `{name}` | {required} | {desc} |\n"
    else:
        secrets_text = "_This workflow does not require any secrets._"
    
    # ========== FORMAT JOBS ==========
    if jobs:
        jobs_text = ""
        for job_name, job_config in jobs.items():
            if not isinstance(job_config, dict):
                continue
            
            jobs_text += f"### 🔧 `{job_name}`\n\n"
            
            # Job metadata
            runs_on = job_config.get('runs-on', '')
            if runs_on:
                jobs_text += f"**Runs on:** `{runs_on}`\n\n"
            
            # Steps
            steps = job_config.get('steps', [])
            if steps:
                jobs_text += "| Step | Uses | Run Command |\n"
                jobs_text += "| ---- | ---- | ----------- |\n"
                for i, step in enumerate(steps, 1):
                    if not isinstance(step, dict):
                        continue
                    
                    name = step.get('name', f'Step {i}')
                    uses = step.get('uses', '')
                    run_cmd = step.get('run', '')
                    
                    # Format run command
                    if run_cmd:
                        run_display = ' '.join(str(run_cmd).strip().split())
                        if len(run_display) > 50:
                            run_display = '✅ Yes (see YAML)'
                        else:
                            run_display = f'`{run_display}`'
                    else:
                        run_display = ''
                    
                    uses_display = f'`{uses}`' if uses else ''
                    jobs_text += f"| {name} | {uses_display} | {run_display} |\n"
                
                jobs_text += "\n"
            else:
                jobs_text += "_No steps defined._\n\n"
    else:
        jobs_text = "_This workflow has no jobs defined._"
    
    # ========== READ FULL YAML ==========
    with open(workflow_file, 'r') as f:
        full_yaml = f.read().rstrip()
    
    # ========== GENERATE DATE ==========
    generation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # ========== CREATE README ==========
    workflow_file_name = Path(workflow_file).name
    
    readme = f"""# {workflow_name}

> **Type:** {workflow_type}  
> **Source:** `{workflow_file_name}`

## 📋 Overview

This document provides comprehensive documentation for the `{workflow_name}` workflow.

---

## 🎯 Triggers

{triggers_text}

---

## 📥 Inputs

{inputs_text}

---

## 📤 Outputs

{outputs_text}

---

## 🔐 Secrets

{secrets_text}

---

## 💼 Jobs

{jobs_text}

---

## 📄 Full Workflow YAML

<details>
<summary>Click to expand full YAML definition</summary>

```yaml
{full_yaml}
```

</details>

---

**Generated on:** {generation_date}  
**Last Updated:** Check the workflow file history for the most recent changes.
"""
    
    # Write output
    with open(output_file, 'w') as f:
        f.write(readme)
    
    print(f"✅ Created: {output_file}")
    print(f"   Size: {len(readme)} bytes")

if __name__ == '__main__':
    main()
