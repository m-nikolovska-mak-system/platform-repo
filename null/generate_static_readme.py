#!/usr/bin/env python3
import argparse
from datetime import datetime

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    print("📄 Using template:", args.template)
    print("📄 Writing to:", args.output)

    with open(args.template, "r", encoding="utf8") as f:
        template = f.read()

    # Hard-coded, guaranteed values
    data = {
        "{{TITLE}}": "Static Test Title",
        "{{DATE}}": datetime.now().strftime("%Y-%m-%d"),
        "{{TRIGGERS}}": "- static trigger A\n- static trigger B",
        "{{INPUTS}}": "- input A: value\n- input B: value",
        "{{OUTPUTS}}": "- output A\n- output B",
        "{{SECRETS}}": "- SECRET_A\n- SECRET_B",
    }

    filled = template
    for placeholder, value in data.items():
        filled = filled.replace(placeholder, value)

    with open(args.output, "w", encoding="utf8") as f:
        f.write(filled)

    print("✅ Static README generated successfully")

if __name__ == "__main__":
    main()
