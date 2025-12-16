#!/bin/bash
set -e

WORKFLOW_FILE="$1"
OUTPUT_FILE="$2"
TEMPLATE_FILE="$3"

# Extract workflow name
WORKFLOW_NAME=$(yq eval '.name' "$WORKFLOW_FILE")
SOURCE_FILE=$(basename "$WORKFLOW_FILE")

# Start building the documentation
cat "$TEMPLATE_FILE" > "$OUTPUT_FILE"

# Add the header section
cat >> "$OUTPUT_FILE" << EOF

# ${WORKFLOW_NAME}
**Source:** \`${SOURCE_FILE}\`

## Triggers
EOF

# Extract triggers
yq eval '.on | keys | .[]' "$WORKFLOW_FILE" | while read -r trigger; do
  echo "- \`$trigger\`" >> "$OUTPUT_FILE"
done

# Extract inputs if workflow_call exists
if yq eval '.on.workflow_call.inputs' "$WORKFLOW_FILE" | grep -v "null" > /dev/null 2>&1; then
  cat >> "$OUTPUT_FILE" << EOF

## Inputs
| name | type | required | default | description |
| --- | --- | --- | --- | --- |
EOF
  
  yq eval '.on.workflow_call.inputs | to_entries | .[]' "$WORKFLOW_FILE" -o=json | jq -r '
    .key as $name |
    .value |
    "| \($name) | \(.type // "string") | \(if .required then "yes" else "no" end) | \(.default // "") | \(.description // "") |"
  ' >> "$OUTPUT_FILE"
else
  echo -e "\n## Inputs\n_None_" >> "$OUTPUT_FILE"
fi

# Extract outputs if they exist
if yq eval '.on.workflow_call.outputs' "$WORKFLOW_FILE" | grep -v "null" > /dev/null 2>&1; then
  cat >> "$OUTPUT_FILE" << EOF

## Outputs
| name | description |
| --- | --- |
EOF
  
  yq eval '.on.workflow_call.outputs | to_entries | .[]' "$WORKFLOW_FILE" -o=json | jq -r '
    .key as $name |
    .value |
    "| \($name) | \(.description // "") |"
  ' >> "$OUTPUT_FILE"
else
  echo -e "\n## Outputs\n_None_" >> "$OUTPUT_FILE"
fi

# Extract secrets if they exist
if yq eval '.on.workflow_call.secrets' "$WORKFLOW_FILE" | grep -v "null" > /dev/null 2>&1; then
  cat >> "$OUTPUT_FILE" << EOF

## Secrets
| name | required | description |
| --- | --- | --- |
EOF
  
  yq eval '.on.workflow_call.secrets | to_entries | .[]' "$WORKFLOW_FILE" -o=json | jq -r '
    .key as $name |
    .value |
    "| \($name) | \(if .required then "yes" else "no" end) | \(.description // "") |"
  ' >> "$OUTPUT_FILE"
else
  echo -e "\n## Secrets\n_None_" >> "$OUTPUT_FILE"
fi

# Extract jobs
cat >> "$OUTPUT_FILE" << EOF

## Jobs
EOF

yq eval '.jobs | keys | .[]' "$WORKFLOW_FILE" | while read -r job_name; do
  echo -e "\n### ${job_name}" >> "$OUTPUT_FILE"
  echo "| name | action | run |" >> "$OUTPUT_FILE"
  echo "| --- | --- | --- |" >> "$OUTPUT_FILE"
  
  yq eval ".jobs.${job_name}.steps[]" "$WORKFLOW_FILE" -o=json | jq -r '
    .name as $name |
    (.uses // "") as $action |
    (if .run then "`run` command" else "" end) as $run |
    "| \($name) | \($action) | \($run) |"
  ' >> "$OUTPUT_FILE"
done

# Add full YAML section
cat >> "$OUTPUT_FILE" << EOF

## Full YAML
\`\`\`yaml
$(cat "$WORKFLOW_FILE")
\`\`\`
EOF

echo "✅ Documentation generated: $OUTPUT_FILE"
