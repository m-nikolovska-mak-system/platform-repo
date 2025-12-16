#!/usr/bin/env python3
"""
extract.py

Usage:
  python3 scripts/extract.py path/to/workflow.yml path/to/output.md
Options:
  --dry-run    : print what would be written but don't write the file
  --verbose    : print debug messages
"""

from __future__ import annotations
import argparse
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

ESCAPE_BACKTICK = lambda s: s.replace("`", "\\`") if isinstance(s, str) else s

def load_workflow(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if data is None:
                return {}
            if not isinstance(data, dict):
                raise ValueError("Top-level YAML is not a mapping/dict.")
            return data
    except Exception as e:
        raise RuntimeError(f"Failed to read/parse YAML: {e}")

def detect_on_section(wf: Dict[str, Any]):
    """
    Robustly find the 'on' section in workflow YAML.
    Handles:
      - on: <mapping>
      - on: push
      - on: [push, pull_request]
      - YAML quirk where key True was parsed instead of 'on'
    Returns (original_key, value)
    """
    if "on" in wf:
        return "on", wf["on"]
    # fallback: sometimes YAML parsers can turn certain strings/keys into booleans
    # check for boolean True key (observed quirk)
    for k in wf.keys():
        if k is True or (isinstance(k, str) and k.strip().lower() == "on"):
            return k, wf[k]
    return None, None

def normalize_triggers(on_section) -> List[str]:
    if on_section is None:
        return []
    if isinstance(on_section, dict):
        return list(on_section.keys())
    if isinstance(on_section, list):
        # sometimes 'on' can be a sequence of events
        return [str(x) for x in on_section]
    if isinstance(on_section, str):
        return [on_section]
    if isinstance(on_section, bool) and on_section is True:
        # shorthand 'on: true' means "enabled for all events" in some contexts
        return ["<all>"]
    return []

def format_inputs(inputs: Dict[str, Any]) -> str:
    if not inputs:
        return "_This workflow does not accept any inputs._"
    lines = [
        "| Name | Type | Required | Default | Description |",
        "| ---- | ---- | -------- | ------- | ----------- |",
    ]
    for name, props in inputs.items():
        if props is None:
            props = {}
        inp_type = props.get("type", "string")
        required = "✅ Yes" if props.get("required", False) else "❌ No"
        default = props.get("default", "_not set_")
        desc = ESCAPE_BACKTICK(props.get("description", "_No description provided_"))
        lines.append(f"| `{name}` | `{inp_type}` | {required} | `{default}` | {desc} |")
    return "\n".join(lines)

def format_outputs(outputs: Dict[str, Any]) -> str:
    if not outputs:
        return "_This workflow does not expose any outputs._"
    lines = [
        "| Name | Description | Value |",
        "| ---- | ----------- | ----- |",
    ]
    for name, props in outputs.items():
        if props is None:
            props = {}
        desc = ESCAPE_BACKTICK(props.get("description", "_No description provided_"))
        value = props.get("value", "_not specified_")
        vstr = str(value)
        if len(vstr) > 80:
            vstr = vstr[:77] + "..."
        lines.append(f"| `{name}` | {desc} | `{ESCAPE_BACKTICK(vstr)}` |")
    return "\n".join(lines)

def format_secrets(secrets: Dict[str, Any]) -> str:
    if not secrets:
        return "_This workflow does not require any secrets._"
    lines = [
        "| Name | Required | Description |",
        "| ---- | -------- | ----------- |",
    ]
    for name, props in secrets.items():
        if props is None:
            props = {}
        required = "✅ Yes" if props.get("required", False) else "❌ No"
        desc = ESCAPE_BACKTICK(props.get("description", "_No description provided_"))
        lines.append(f"| `{name}` | {required} | {desc} |")
    return "\n".join(lines)

def summarize_jobs(jobs: Dict[str, Any]) -> str:
    if not jobs:
        return "_This workflow has no jobs defined._"
    out_lines: List[str] = []
    for job_name, job_cfg in jobs.items():
        if not isinstance(job_cfg, dict):
            continue
        out_lines.append(f"### 🔧 `{job_name}`\n")
        runs_on = job_cfg.get("runs-on") or job_cfg.get("runs_on") or ""
        if runs_on:
            out_lines.append(f"**Runs on:** `{runs_on}`\n")
        steps = job_cfg.get("steps", [])
        if steps:
            out_lines.append("| Step | Uses | Run |\n| ---- | ---- | --- |")
            for i, step in enumerate(steps, 1):
                if not isinstance(step, dict):
                    continue
                name = ESCAPE_BACKTICK(step.get("name", f"Step {i}"))
                uses = step.get("uses", "")
                run_cmd = step.get("run", "")
                # If run command is long, don't inline it - indicate presence
                if isinstance(run_cmd, str):
                    run_display = run_cmd.strip().replace("\n", " ")
                    if len(run_display) > 70:
                        run_display = "✅ Yes (see full YAML)"
                    else:
                        run_display = f"`{ESCAPE_BACKTICK(run_display)}`"
                else:
                    run_display = ""
                uses_display = f"`{uses}`" if uses else ""
                out_lines.append(f"| {name} | {uses_display} | {run_display} |")
            out_lines.append("")  # blank line
        else:
            out_lines.append("_No steps defined._\n")
    return "\n".join(out_lines)

def build_readme(content: Dict[str, Any], source_path: Path) -> str:
    workflow_name = content.get("name", "Unnamed Workflow")
    key, on_section = detect_on_section(content)
    triggers = normalize_triggers(on_section)
    # inputs/outputs/secrets mainly come from workflow_call or workflow_dispatch
    inputs = {}
    outputs = {}
    secrets = {}
    if isinstance(on_section, dict):
        wf_call = on_section.get("workflow_call")
        if isinstance(wf_call, dict):
            inputs = wf_call.get("inputs", {}) or {}
            outputs = wf_call.get("outputs", {}) or {}
            secrets = wf_call.get("secrets", {}) or {}
        wf_dispatch = on_section.get("workflow_dispatch")
        if isinstance(wf_dispatch, dict):
            # merge dispatch inputs (dispatch inputs may be separate)
            inputs = {**inputs, **(wf_dispatch.get("inputs", {}) or {})}

    jobs = content.get("jobs", {}) or {}
    workflow_types = []
    if "workflow_call" in triggers:
        workflow_types.append("Reusable Workflow")
    if "workflow_dispatch" in triggers:
        workflow_types.append("Manual Dispatch")
    if any(t in triggers for t in ["push", "pull_request", "schedule", "release"]):
        workflow_types.append("Automated")
    workflow_type = " + ".join(workflow_types) if workflow_types else "Standard Workflow"

    # read full YAML safely for the code block; escape triple backticks
    try:
        with source_path.open("r", encoding="utf-8") as fh:
            full_yaml = fh.read().rstrip()
            full_yaml = full_yaml.replace("```", "``\\`")  # avoid breaking MD code fence
    except Exception:
        full_yaml = "<unable to read source YAML>"

    generation_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    readme = f"""# {ESCAPE_BACKTICK(workflow_name)}

> **Type:** {workflow_type}  
> **Source:** `{source_path.name}`

## 📋 Overview

This document provides comprehensive documentation for the `{ESCAPE_BACKTICK(workflow_name)}` workflow.

---

## 🎯 Triggers

"""
    if triggers:
        for t in triggers:
            readme += f"- **`{t}`**\n"
            # print some details if available
            if isinstance(on_section, dict) and t in on_section and isinstance(on_section[t], dict):
                cfg = on_section[t]
                if "branches" in cfg:
                    br = cfg["branches"]
                    readme += f"  - Branches: `{', '.join(br) if isinstance(br, list) else br}`\n"
                if "paths" in cfg:
                    paths = cfg["paths"]
                    if isinstance(paths, list):
                        includes = [p for p in paths if not p.startswith("!")]
                        excludes = [p[1:] for p in paths if p.startswith("!")]
                        if includes:
                            readme += f"  - Paths (includes): `{', '.join(includes)}`\n"
                        if excludes:
                            readme += f"  - Paths (excludes): `{', '.join(excludes)}`\n"
                if "types" in cfg:
                    types = cfg["types"]
                    readme += f"  - Types: `{', '.join(types) if isinstance(types, list) else types}`\n"
                if t == "schedule" and isinstance(cfg, list):
                    readme += "  - Cron schedules:\n"
                    for sched in cfg:
                        cron = sched.get("cron") if isinstance(sched, dict) else None
                        if cron:
                            readme += f"    - `{cron}`\n"
    else:
        readme += "_No triggers defined._\n"

    readme += "\n---\n\n## 📥 Inputs\n\n"
    readme += format_inputs(inputs) + "\n\n---\n\n## 📤 Outputs\n\n"
    readme += format_outputs(outputs) + "\n\n---\n\n## 🔐 Secrets\n\n"
    readme += format_secrets(secrets) + "\n\n---\n\n## 💼 Jobs\n\n"
    readme += summarize_jobs(jobs) + "\n\n---\n\n## 📄 Full Workflow YAML\n\n<details>\n<summary>Click to expand full YAML definition</summary>\n\n```yaml\n" + full_yaml + "\n```\n\n</details>\n\n---\n\n**Generated on:** " + generation_date + "\n"
    return readme

def main(argv=None):
    argv = argv or sys.argv[1:]
    parser = argparse.ArgumentParser(description="Extract GitHub Actions workflow into README markdown.")
    parser.add_argument("workflow_file", type=Path, help="Path to workflow YAML")
    parser.add_argument("output_file", type=Path, help="Path to output README.md")
    parser.add_argument("--dry-run", action="store_true", help="Do not write file, just print summary")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output for debugging")
    args = parser.parse_args(argv)

    if not args.workflow_file.exists():
        print(f"❌ Error: workflow file not found: {args.workflow_file}", file=sys.stderr)
        return 2

    try:
        workflow = load_workflow(args.workflow_file)
    except Exception as e:
        print(f"❌ {e}", file=sys.stderr)
        return 3

    readme_text = build_readme(workflow, args.workflow_file)

    if args.dry_run or args.verbose:
        # print a short preview to stdout
        preview = "\n".join(readme_text.splitlines()[:40])
        print("----- README PREVIEW (first 40 lines) -----")
        print(preview)
        print("----- end preview -----\n")

    if args.dry_run:
        print("Dry-run mode: not writing output file.")
        return 0

    # ensure parent exists
    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    try:
        args.output_file.write_text(readme_text, encoding="utf-8")
        size = args.output_file.stat().st_size
        print(f"✅ Created: {args.output_file} ({size} bytes)")
        return 0
    except Exception as e:
        print(f"❌ Failed to write output: {e}", file=sys.stderr)
        return 4

if __name__ == "__main__":
    raise SystemExit(main())
