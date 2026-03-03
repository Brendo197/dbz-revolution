@echo off
title DBZ Revolution - Client Compiler

REM ===== ATIVAR AMBIENTE VIRTUAL =====
if not exist .venv\Scripts\activate.bat (
    echo [ERRO] Ambiente virtual nao encontrado!
    echo Crie com: python -m venv .venv
    timeout /t 5 >nul
    exit
)

call .venv\Scripts\activate.bat

REM ===== LIMPAR BUILDS ANTIGOS =====
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "DBZ Revolution.spec" del "DBZ Revolution.spec"

REM ===== COMPILAR CLIENT =====
pyinstaller ^
  --onefile ^
  --windowed ^
  --clean ^
  --name "DBZ Revolution" ^
  --icon "assets\ui\icon.ico" ^
  --add-data "assets;assets" ^
  -p . ^
  --collect-submodules launcher ^
  --collect-submodules launcher.screens ^
  --collect-submodules launcher.ui ^
  --collect-submodules network ^
  --collect-submodules protocol ^
  --collect-submodules game ^
  --collect-submodules core ^
  run_client.py

REM ===== FINALIZAR =====
echo.
echo [OK] Compilacao finalizada com sucesso.
timeout /t 3 >nul
exit
