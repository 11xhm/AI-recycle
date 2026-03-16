@echo off
setlocal
set SCRIPT_DIR=%~dp0
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%start-dev.ps1"
if errorlevel 1 (
  echo.
  echo 启动失败，请把上面的报错内容复制给我。
  pause
)
