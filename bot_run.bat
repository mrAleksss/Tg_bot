@echo off

call %~dp0telegram_bot\venv\Scripts\activate

cd %~dp0telegram_bot

set TOKEN=5716687419:AAGE9xwr2mgbdKvhHkZ-57pSkqfmgeQJvDs

python bot_telegram.py

pause