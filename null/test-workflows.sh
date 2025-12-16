#!/bin/bash
set -e

echo "🧪 Running all test workflows locally with ACT..."

for wf in .github/workflows/*.yml; do
  echo "▶️ Testing $wf ..."
  act -W "$wf" --dryrun || {
    echo "❌ Workflow $wf failed!"
    exit 1
  }
done

echo "✅ All workflows passed!"
