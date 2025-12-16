import os
import yaml
from datetime import datetime
from pathlib import Path

# ConfigurationNSS yhis is a comment hi hello here
CONFIG_PATH = "action.yml"  # or .yaml
README_PATH = "README.md"

def load_config(path):
    """Load and parse YAML configuration file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Configuration file not found: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def generate_badges(config):
    """Generate badge section from config."""
    badges = config.get("badges", [])
    if not badges:
        return ""
    
    badge_lines = []
    for badge in badges:
        if badge.get("type") == "shield":
            badge_lines.append(
                f"![{badge['alt']}](https://img.shields.io/badge/{badge['label']}-{badge['message']}-{badge['color']})"
            )
        elif badge.get("url") and badge.get("alt"):
            badge_lines.append(f"![{badge['alt']}]({badge['url']})")
    
    return "\n".join(badge_lines) + "\n" if badge_lines else ""

def generate_features(config):
    """Generate features section from config."""
    features = config.get("features", [])
    if not features:
        return ""
    
    section = "\n## ✨ Features\n\n"
    for feature in features:
        section += f"- **{feature['title']}**: {feature['description']}\n"
    
    return section

def generate_installation(config):
    """Generate installation section from config."""
    install = config.get("installation", {})
    if not install:
        return ""
    
    section = "\n## 📦 Installation\n\n"
    
    if install.get("prerequisites"):
        section += "### Prerequisites\n\n"
        for prereq in install["prerequisites"]:
            section += f"- {prereq}\n"
        section += "\n"
    
    if install.get("steps"):
        section += "### Steps\n\n"
        for i, step in enumerate(install["steps"], 1):
            section += f"{i}. {step['description']}\n"
            if step.get("command"):
                section += f"   ```bash\n   {step['command']}\n   ```\n"
            section += "\n"
    
    return section

def generate_usage(config):
    """Generate usage section from config."""
    usage = config.get("usage", {})
    if not usage:
        return ""
    
    section = "\n## 🚀 Usage\n\n"
    
    if usage.get("description"):
        section += f"{usage['description']}\n\n"
    
    if usage.get("examples"):
        section += "### Examples\n\n"
        for example in usage["examples"]:
            section += f"**{example['title']}**\n\n"
            if example.get("description"):
                section += f"{example['description']}\n\n"
            if example.get("code"):
                lang = example.get("language", "bash")
                section += f"```{lang}\n{example['code']}\n```\n\n"
    
    return section

def generate_configuration(config):
    """Generate configuration section from config."""
    cfg = config.get("configuration", {})
    if not cfg:
        return ""
    
    section = "\n## ⚙️ Configuration\n\n"
    
    if cfg.get("description"):
        section += f"{cfg['description']}\n\n"
    
    if cfg.get("options"):
        section += "| Option | Type | Default | Description |\n"
        section += "|--------|------|---------|-------------|\n"
        for opt in cfg["options"]:
            section += f"| `{opt['name']}` | {opt['type']} | `{opt.get('default', '-')}` | {opt['description']} |\n"
        section += "\n"
    
    return section

def generate_api_docs(config):
    """Generate API documentation section from config."""
    api = config.get("api", {})
    if not api:
        return ""
    
    section = "\n## 📚 API Documentation\n\n"
    
    if api.get("endpoints"):
        for endpoint in api["endpoints"]:
            section += f"### `{endpoint['method']}` {endpoint['path']}\n\n"
            section += f"{endpoint['description']}\n\n"
            
            if endpoint.get("parameters"):
                section += "**Parameters:**\n\n"
                for param in endpoint["parameters"]:
                    required = "Required" if param.get("required") else "Optional"
                    section += f"- `{param['name']}` ({param['type']}, {required}): {param['description']}\n"
                section += "\n"
            
            if endpoint.get("response"):
                section += "**Response:**\n\n"
                section += f"```json\n{endpoint['response']}\n```\n\n"
    
    return section

def generate_contributing(config):
    """Generate contributing section from config."""
    contrib = config.get("contributing")
    if not contrib:
        return ""
    
    section = "\n## 🤝 Contributing\n\n"
    section += f"{contrib}\n"
    
    return section

def generate_license(config):
    """Generate license section from config."""
    license_info = config.get("license")
    if not license_info:
        return ""
    
    section = "\n## 📄 License\n\n"
    section += f"{license_info}\n"
    
    return section

def generate_readme(config):
    """Generate complete README content from config."""
    project = config.get("project", {})
    
    # Header
    readme = f"# {project.get('name', 'Project Name')}\n\n"
    
    # Badges
    readme += generate_badges(config)
    
    # Description
    if project.get("description"):
        readme += f"\n{project['description']}\n"
    
    # Table of Contents (optional)
    if config.get("include_toc", True):
        readme += "\n## 📋 Table of Contents\n\n"
        sections = [
            ("Features", "features"),
            ("Installation", "installation"),
            ("Usage", "usage"),
            ("Configuration", "configuration"),
            ("API Documentation", "api-documentation"),
            ("Contributing", "contributing"),
            ("License", "license"),
        ]
        for title, anchor in sections:
            if config.get(anchor.replace("-", "_")) or config.get(anchor.split("-")[0]):
                readme += f"- [{title}](#{anchor})\n"
        readme += "\n"
    
    # Generate all sections
    readme += generate_features(config)
    readme += generate_installation(config)
    readme += generate_usage(config)
    readme += generate_configuration(config)
    readme += generate_api_docs(config)
    readme += generate_contributing(config)
    readme += generate_license(config)
    
    # Footer with timestamp
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    readme += f"\n---\n\n_Last generated: {timestamp}_\n"
    
    return readme

def main():
    """Main function to generate README from YAML config."""
    try:
        print(f"📖 Loading configuration from {CONFIG_PATH}...")
        config = load_config(CONFIG_PATH)
        
        print("🔨 Generating README content...")
        readme_content = generate_readme(config)
        
        print(f"💾 Writing README to {README_PATH}...")
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        print(f"✅ README successfully generated at {README_PATH}")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("\n💡 Tip: Create a config.yml file with your project details.")
    except yaml.YAMLError as e:
        print(f"❌ YAML parsing error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
