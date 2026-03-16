#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_PORT="${FRONTEND_PORT:-5173}"
BACKEND_PORT="${BACKEND_PORT:-8000}"

cd "$ROOT_DIR"
mkdir -p logs

cd frontend
npm ci
npm run build

cd "$ROOT_DIR"
if ! command -v pm2 >/dev/null 2>&1; then
  echo "pm2 未安装，请先执行：npm i -g pm2"
  exit 1
fi

pm2 delete recycle-ai-frontend >/dev/null 2>&1 || true
pm2 serve "$ROOT_DIR/frontend/dist" "$FRONTEND_PORT" --name recycle-ai-frontend --spa

cd "$ROOT_DIR"
exec gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b "0.0.0.0:${BACKEND_PORT}" backend.main:app \
  --access-logfile "$ROOT_DIR/logs/backend-access.log" \
  --error-logfile "$ROOT_DIR/logs/backend-error.log"
