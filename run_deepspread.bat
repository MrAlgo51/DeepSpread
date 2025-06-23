@echo off
setlocal

rem Log timestamp to last_run.txt
echo [MERGED LOGGER] %DATE% %TIME% >> logs\last_run.txt

rem Change to project directory and run script
cd /d %~dp0
start "DeepSpread Logger" cmd /k python src\merged_logger.py

endlocal

