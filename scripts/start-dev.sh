#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if command -v tmux >/dev/null 2>&1; then
  SESSION="recycle-ai-dev"
  tmux has-session -t "$SESSION" 2>/dev/null && tmux kill-session -t "$SESSION"
  tmux new-session -d -s "$SESSION" -c "$ROOT_DIR"
  tmux send-keys -t "$SESSION":0 "cd \"$ROOT_DIR/backend\" && uvicorn main:app --reload --port 8000" C-m
  tmux split-window -h -t "$SESSION":0 -c "$ROOT_DIR"
  tmux send-keys -t "$SESSION":0.1 "cd \"$ROOT_DIR/frontend\" && npm run dev" C-m
  tmux select-pane -t "$SESSION":0.0
  tmux attach -t "$SESSION"
  exit 0
fi

cd "$ROOT_DIR"
mkdir -p logs

(
  cd backend
  uvicorn main:app --reload --port 8000 2>&1 | sed -u 's/^/[backend] /'
) &
BACK_PID=$!

(
  cd frontend
  npm run dev 2>&1 | sed -u 's/^/[frontend] /'
) &
FRONT_PID=$!

cleanup() {
  kill "$BACK_PID" "$FRONT_PID" >/dev/null 2>&1 || true
}
trap cleanup EXIT INT TERM

wait "$BACK_PID" "$FRONT_PID"
