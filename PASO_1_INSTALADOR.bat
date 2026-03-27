@echo off
setlocal
title Instalador Magica Canva Studio 🪄

echo ====================================================
echo    INSTALADOR AUTOMATICO PARA LA MADRINA
echo ====================================================
echo.

:: 1. Comprobar e Instalar Python (vía Winget)
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python no detectado. Instalando...
    winget install -e --id Python.Python.3.11 --accept-package-agreements --accept-source-agreements
    echo [!] IMPORTANTE: Reinicia este script despues de que termine la instalacion de Python.
    pause
    exit
) else (
    echo [OK] Python detectado.
)

:: 2. Comprobar e Instalar Node.js (vía Winget)
node -v >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Node.js no detectado. Instalando...
    winget install -e --id OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements
    echo [!] IMPORTANTE: Reinicia este script despues de que termine la instalacion de Node.
    pause
    exit
) else (
    echo [OK] Node.js detectado.
)

echo.
echo [1/3] Configurando Backend (IA)...
cd backend
if not exist venv (
    echo Creando entorno virtual...
    python -m venv venv
)
echo Instalando librerias del servidor...
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo [EXTRA] Descargando cerebro de IA (esto puede tardar minutos)...
:: Usamos el python del venv directamente para asegurar que funcione
venv\Scripts\python.exe warmup.py
cd ..

echo.
echo [2/3] Configurando Frontend (Interfaz)...
cd frontend
echo Instalando modulos de la interfaz...
call npm install
cd ..

echo.
echo [3/3] Creando lanzador invisible...
:: Crear el script VBS para que no se vean ventanas negras al usarlo
echo Set WshShell = CreateObject("WScript.Shell") > "Mágica Canva.vbs"
echo WshShell.Run chr(34) ^& "%~dp0INICIAR_APP.bat" ^& Chr(34), 0 >> "Mágica Canva.vbs"
echo Set WshShell = Nothing >> "Mágica Canva.vbs"

echo.
echo ====================================================
echo   ¡TODO LISTO, MADRINA! 
echo.
echo   1. Mueve el archivo "Magica Canva.vbs" al escritorio.
echo   2. Usa ese icono para abrir tu programa.
echo ====================================================
pause