@echo off
:: Iniciar Backend
cd /d "%~dp0backend"
start /min cmd /c "venv\Scripts\activate && uvicorn main:app --port 8000"

:: Iniciar Frontend
cd /d "%~dp0frontend"
start /min cmd /c "npm run dev"

:: Esperar a que los puertos esten listos
timeout /t 6 /nobreak > nul

:: Abrir el navegador en la App
start http://localhost:5173