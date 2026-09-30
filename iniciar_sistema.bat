@echo off
title Sistema de Controle Financeiro Rural - UniRV
echo ========================================================
echo    SISTEMA DE CONTROLE FINANCEIRO RURAL - UNIRV
echo    Avaliacao N2 - Etapa 1: Extrator Fiscal com IA Gemini
echo ========================================================
echo.

cd /d "%~dp0"

:: 1. Tenta comando python global
where python >nul 2>nul
if %errorlevel% equ 0 (
    set "PY_CMD=python"
    goto RUN
)

:: 2. Tenta launcher py
where py >nul 2>nul
if %errorlevel% equ 0 (
    set "PY_CMD=py"
    goto RUN
)

:: 3. Fallback para caminho local se aplicável
if exist "C:\Program Files\TacticalAgent\python\py3.14.5_amd64\python.exe" (
    set "PY_CMD=C:\Program Files\TacticalAgent\python\py3.14.5_amd64\python.exe"
    goto RUN
)

echo [ERRO] Python nao foi encontrado no sistema!
echo Certifique-se de que o Python esteja instalado e marcado na opcao "Add Python to PATH".
echo.
pause
exit /b 1

:RUN
echo Executavel Python detectado: %PY_CMD%
echo.
echo Verificando banco de dados...
"%PY_CMD%" manage.py migrate --noinput >nul 2>nul
echo.
echo ========================================================
echo  Servidor ativo em: http://127.0.0.1:8000/
echo  Abra o link acima no navegador (Chrome, Edge, etc.)
echo ========================================================
echo.
"%PY_CMD%" manage.py runserver 127.0.0.1:8000
pause
