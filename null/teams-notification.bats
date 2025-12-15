#!/usr/bin/env bats

setup() {
  export SCRIPT_PATH="bash ./scripts/send-teams-notification.sh"
  
  # Create a mock curl command
  export PATH="$BATS_TEST_TMPDIR:$PATH"
  
  cat > "$BATS_TEST_TMPDIR/curl" << 'EOF'
#!/bin/bash
# Mock curl for testing
if [[ "$*" =~ "status/200" ]]; then
  echo "200"
elif [[ "$*" =~ "status/202" ]]; then
  echo "202"
elif [[ "$*" =~ "status/500" ]]; then
  echo "500"
else
  echo "200"
fi
EOF
  chmod +x "$BATS_TEST_TMPDIR/curl"
}

@test "script fails when TEAMS_WEBHOOK_URL is missing" {
  unset TEAMS_WEBHOOK_URL
  export NOTIFICATION_TITLE="Test"
  run $SCRIPT_PATH
  [ "$status" -eq 1 ]
  [[ "$output" =~ "TEAMS_WEBHOOK_URL is not set" ]]
}

@test "script fails when NOTIFICATION_TITLE is missing" {
  export TEAMS_WEBHOOK_URL="https://httpbin.org/status/200"
  unset NOTIFICATION_TITLE
  run $SCRIPT_PATH
  [ "$status" -eq 1 ]
  [[ "$output" =~ "NOTIFICATION_TITLE is not set" ]]
}

@test "script succeeds with 200 response" {
  export TEAMS_WEBHOOK_URL="https://test.com/status/200"
  export NOTIFICATION_TITLE="Deploy Success"
  run $SCRIPT_PATH
  [ "$status" -eq 0 ]
  [[ "$output" =~ "notification sent successfully" ]]
}

@test "script succeeds with 202 response" {
  export TEAMS_WEBHOOK_URL="https://test.com/status/202"
  export NOTIFICATION_TITLE="Deploy Success"
  run $SCRIPT_PATH
  [ "$status" -eq 0 ]
  [[ "$output" =~ "notification sent successfully" ]]
}

@test "script uses default action message when not provided" {
  export TEAMS_WEBHOOK_URL="https://test.com/status/200"
  export NOTIFICATION_TITLE="Test"
  unset ACTION_MESSAGE
  run $SCRIPT_PATH
  [ "$status" -eq 0 ]
}

@test "script handles webhook failure with 500" {
  export TEAMS_WEBHOOK_URL="https://test.com/status/500"
  export NOTIFICATION_TITLE="Test"
  run $SCRIPT_PATH
  [ "$status" -eq 1 ]
  [[ "$output" =~ "webhook failed" ]]
}