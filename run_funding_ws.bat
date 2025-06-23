@echo off
echo [FUNDING LOGGER] %DATE% %TIME% >> logs\last_run.txt
start "" cmd /k python src\binance_premium_ws_logger.py
exit

