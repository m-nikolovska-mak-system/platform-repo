#!/usr/bin/env python3
import argparse
import yaml
from datetime import datetime
import sys

def main():
    parser = argparse.ArgumentParser(description="Generate README from workflow YAML and template")
    parser.add_argument("--workflow", required=True, help="Path to workflow YAML")
    parser.add_argument("--template", required=True, help="Path to template file")
    parser.add_argument("--output", required=True, help="Path to save the generated README")
    args = parser.parse_args()
    
    # Load workflow YAML
    print(f"📖 Reading workflow: {args.workflow}")
    try:
        with open(args.workflow, "r", encoding="utf-8") as f:
            workflow = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"❌ Workflow file not found: {args.workflow}")
        sys.exit(1)
    
    # Get workflow name
    workflow_name = workflow.get("name", "Unnamed Workflow")
    print(f"   Workflow name: {workflow_name}")
    
    # Get the 'on' section
    on_section = workflow.get("on", {})
    print(f"   Triggers found: {list(on_section.keys())}")
    
    # Try to get inputs from BOTH workflow_dispatch AND workflow_call
    inputs = {}
    
    # Check workflow_dispatch first
    if "workflow_dispatch" in on_section:
        dispatch = on_section["workflow_dispatch"]
        if dispatch and isinstance(dispatch, dict):
            dispatch_inputs = dispatch.get("inputs", {})
            inputs.update(dispatch_inputs)
            print(f"   Found workflow_dispatch inputs: {list(dispatch_inputs.keys())}")
    
    # Check workflow_call (reusable workflows)
    if "workflow_call" in on_section:
        call = on_section["workflow_call"]
        if call and isinstance(call, dict):
            call_inputs = call.get("inputs", {})
            inputs.update(call_inputs)
            print(f"   Found workflow_call inputs: {list(call_inputs.keys())}")
    
    print(f"   Total inputs found: {list(inputs.keys())}")
    
    # Extract outputs (only for workflow_call)
    outputs = {}
    if "workflow_call" in on_section:
        call = on_section["workflow_call"]
        if call and isinstance(call, dict):
            outputs = call.get("outputs", {})
            print(f"   Found workflow_call outputs: {list(outputs.keys())}")
    
    # Extract secrets (only for workflow_call)
    secrets = {}
    if "workflow_call" in on_section:
        call = on_section["workflow_call"]
        if call and isinstance(call, dict):
            secrets = call.get("secrets", {})
            print(f"   Found workflow_call secrets: {list(secrets.keys())}")
    
    print()
    
    # Extract values from inputs (use defaults)
    title = workflow_name  # Default to workflow name
    description = "Workflow documentation"  # Default description
    version = "1.0"  # Default version
    
    # If inputs exist, get their default values
    if "title" in inputs and "default" in inputs["title"]:
        title = inputs["title"]["default"]
        print(f"   ✅ Found title: {title}")
    
    if "description" in inputs and "default" in inputs["description"]:
        description = inputs["description"]["default"]
        print(f"   ✅ Found description: {description}")
    
    if "version" in inputs and "default" in inputs["version"]:
        version = inputs["version"]["default"]
        print(f"   ✅ Found version: {version}")
    
    date = datetime.now().strftime("%Y-%m-%d")
    
    print()
    print("📝 Data to fill in template:")
    print(f"   TITLE: {title}")
    print(f"   DESCRIPTION: {description}")
    print(f"   VERSION: {version}")
    print(f"   DATE: {date}")
    print()
    
    data = {
        "{{TITLE}}": title,
        "{{DESCRIPTION}}": description,
        "{{VERSION}}": version,
        "{{DATE}}": date,
    }
    
    # Read template
    print(f"📖 Reading template: {args.template}")
    try:
        with open(args.template, "r", encoding="utf-8") as f:
            template_content = f.read()
    except FileNotFoundError:
        print(f"❌ Template file not found: {args.template}")
        sys.exit(1)
    
    # Replace placeholders
    readme_content = template_content
    for placeholder, value in data.items():
        readme_content = readme_content.replace(placeholder, value)
    
    # Write output
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"✅ README created: {args.output}")
    print(f"   Size: {len(readme_content)} characters")

if __name__ == "__main__":
    main()
