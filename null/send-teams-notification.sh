#!/bin/bash
set -e

# Required environment variables
TEAMS_WEBHOOK_URL="${TEAMS_WEBHOOK_URL:-}"
NOTIFICATION_TITLE="${NOTIFICATION_TITLE:-}"

# Optional with defaults
ACTION_MESSAGE="${ACTION_MESSAGE:-⚠️ Reminder: Changes detected that may require action}"
CARD_COLOR="${CARD_COLOR:-Accent}"

# Validation
if [ -z "$TEAMS_WEBHOOK_URL" ]; then
  echo "❌ Error: TEAMS_WEBHOOK_URL is not set"
  exit 1
fi

if [ -z "$NOTIFICATION_TITLE" ]; then
  echo "❌ Error: NOTIFICATION_TITLE is not set"
  exit 1
fi

# Build payload
PAYLOAD=$(cat <<EOF
{
  "text": "🚀 $NOTIFICATION_TITLE\n$ACTION_MESSAGE"
}
EOF
)

echo "📤 Sending notification to Teams..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" "$TEAMS_WEBHOOK_URL")

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "202" ]; then
  echo "✅ Teams notification sent successfully!"
  exit 0
else
  echo "❌ Error: Teams webhook failed with status $HTTP_CODE"
  exit 1
fi