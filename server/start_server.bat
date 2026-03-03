@echo off
title DBZ REVOLUTION - SERVER

call .venv\Scripts\activate

echo ===============================
echo  DBZ REVOLUTION - SERVER
echo ===============================

echo [1/1] Iniciando servidor...
python run_server.py

pause
