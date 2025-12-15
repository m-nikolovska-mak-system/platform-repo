const fs = require("fs");
const yaml = require("js-yaml");

function generateMarkdown(data, filename) {
  const updated = new Date().toISOString().slice(0, 16).replace("T", " ");

  return `
<div align="center">

# 🚀 ${data.name || "Workflow"}

![Auto-generated](https://img.shields.io/badge/docs-auto--generated-blue?style=flat-square)
![Workflow](https://img.shields.io/badge/type-github--workflow-purple?style=flat-square)
![Updated](https://img.shields.io/badge/updated-${updated}-green?style=flat-square)

</div>

---

## 📋 Overview
> **Workflow File:** \`${filename}\`

## ⚡ Triggers
${formatTriggers(data.on)}

## 🔨 Jobs
${Object.entries(data.jobs || {}).map(formatJob).join("\n\n")}

---

<div align="center">
**📅 Last Updated:** ${updated} UTC  
*Auto-generated documentation. Manual edits will be overwritten.*
</div>
`;
}

function formatTriggers(on) {
  if (!on) return "<em>No triggers defined</em>";

  const rows = Object.keys(on)
    .map(ev => `<tr><td>${ev}</td><td>${JSON.stringify(on[ev])}</td></tr>`)
    .join("\n");

  return `
<table>
<tr><th>Event</th><th>Details</th></tr>
${rows}
</table>`;
}

function formatJob([name, job]) {
  return `
### 🎯 \`${name}\`

**🖥️ Runner:** \`${job["runs-on"] || "N/A"}\`

<details>
<summary>📝 Steps</summary>

${(job.steps || [])
  .map(step => `#### ${step.name || "Step"}\n\`\`\`yaml\n${yaml.dump(step)}\`\`\``)
  .join("\n\n")}
</details>
`;
}

const [workflowFile, outputFile, templateFile] = process.argv.slice(2);

const yamlData = yaml.load(fs.readFileSync(workflowFile, "utf8"));
const autoDoc = generateMarkdown(yamlData, workflowFile);

// Read the template
let template = fs.readFileSync(templateFile, "utf8");

// Replace placeholder block with our auto-doc
template = template.replace(
  /<!-- AUTO-GENERATED-DOCS -->([\s\S]*?)<!-- END-AUTO-GENERATED-DOCS -->/,
  `<!-- AUTO-GENERATED-DOCS -->\n${autoDoc}\n<!-- END-AUTO-GENERATED-DOCS -->`
);

fs.writeFileSync(outputFile, template);

console.log("Generated:", outputFile);
