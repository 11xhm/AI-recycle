#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PYTHON_BIN="${PYTHON_BIN:-python}"
NODE_BIN="${NODE_BIN:-node}"
NPM_BIN="${NPM_BIN:-npm}"

cd "$ROOT_DIR"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "未找到 python，请安装 Python 3.9+"
  exit 1
fi

PY_VER="$("$PYTHON_BIN" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
REQ_PY="3.9"
if "$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,9) else 1)'; then
  echo "Python $PY_VER OK"
else
  echo "Python 版本过低：$PY_VER（需要 >= $REQ_PY）"
  exit 1
fi

echo "安装后端依赖..."
"$PYTHON_BIN" -m pip install -r backend/requirements.txt

if command -v "$NODE_BIN" >/dev/null 2>&1 && command -v "$NPM_BIN" >/dev/null 2>&1; then
  NODE_VER="$("$NODE_BIN" -p 'process.versions.node')"
  echo "Node $NODE_VER OK"
  echo "安装前端依赖..."
  cd "$ROOT_DIR/frontend"
  "$NPM_BIN" ci
else
  echo "未检测到 node/npm，跳过前端依赖安装（需要 Node 18+）"
fi

echo "完成"
