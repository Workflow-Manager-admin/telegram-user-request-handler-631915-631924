#!/bin/bash
cd /tmp/kavia/workspace/code-generation/telegram-user-request-handler-631915-631924/telegram_bot_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

