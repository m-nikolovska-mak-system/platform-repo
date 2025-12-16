import os
import yaml
from pathlib import Path

# Paths this is a test
ROOT = Path(".")
WORKFLOWS_DIR = ROOT / ".github" / "workflows"
ACTION_FILE = ROOT / "action.yml"
README_FILE = ROOT / "README.md"
WORKFLOWS_DOC = ROOT / "docs" / "workflows.md"

def parse_yaml(file_path):
    """Parse a YAML file and return its content as a dictionary."""
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def format_table(title, data):
    """Format a Markdown table for inputs, outputs, or secrets."""
    if not data:
        return f"### {title}\n\n_No {title.lower()} defined._\n\n"
    md = f"### {title}\n\n| Name | Required | Default | Description |\n|------|----------|---------|-------------|\n"
    for name, props in data.items():
        md += f"| `{name}` | {props.get('required', False)} | `{props.get('default', '-')}` | {props.get('description', '-') } |\n"
    md += "\n"
    return md

def generate_action_docs(action_data):
    """Generate documentation for the main GitHub Action."""
    docs = f"# {action_data.get('name', 'Action')}\n\n"
    docs += f"**Description:** {action_data.get('description', '-')}\n\n"
    docs += format_table("Inputs", action_data.get("inputs", {}))
    docs += format_table("Outputs", action_data.get("outputs", {}))
    return docs

def generate_workflow_docs(workflows):
    """Generate documentation for all reusable workflows."""
    docs = "# Reusable Workflows Documentation\n\n"
    for wf_name, wf_data in workflows.items():
        docs += f"## {wf_name}\n\n"
        docs += format_table("Inputs", wf_data.get("inputs", {}))
        docs += format_table("Secrets", wf_data.get("secrets", {}))
    return docs

def main():
    # Process action.yml
    if ACTION_FILE.exists():
        action_data = parse_yaml(ACTION_FILE)
        action_docs = generate_action_docs(action_data)
        README_FILE.write_text(action_docs, encoding="utf-8")
        print(f"✅ Updated {README_FILE}")
    else:
        print("⚠️ No action.yml found.")

    # Process workflows
    workflows_info = {}
    if WORKFLOWS_DIR.exists():
        for wf_file in WORKFLOWS_DIR.glob("*.yml"):
            wf_data = parse_yaml(wf_file)
            if "on" in wf_data and "workflow_call" in wf_data["on"]:
                workflows_info[wf_file.stem] = wf_data["on"]["workflow_call"]
        if workflows_info:
            WORKFLOWS_DOC.parent.mkdir(exist_ok=True)
            WORKFLOWS_DOC.write_text(generate_workflow_docs(workflows_info), encoding="utf-8")
            print(f"✅ Generated {WORKFLOWS_DOC}")
        else:
            print("⚠️ No reusable workflows found.")
    else:
        print("⚠️ No workflows directory found.")

if __name__ == "__main__":
    main()
