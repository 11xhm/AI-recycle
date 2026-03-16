$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$backend = Join-Path $root "backend"
$frontend = Join-Path $root "frontend"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  throw "未找到 python，请先安装 Python 3.9+ 并确保已加入 PATH"
}

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
  throw "未找到 npm，请先安装 Node.js 18+ 并确保已加入 PATH"
}

$backendCmd = "cd `"$backend`"; python -m pip install -r requirements.txt; python -m uvicorn main:app --reload --port 8000"
$frontendCmd = "cd `"$frontend`"; if (!(Test-Path node_modules)) { npm install }; npm run dev"

Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", $backendCmd -WorkingDirectory $backend | Out-Null
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", $frontendCmd -WorkingDirectory $frontend | Out-Null

Start-Sleep -Seconds 2
Start-Process "http://localhost:5173/" | Out-Null
