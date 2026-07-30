@echo off
title Telemetriamaps
cd /d "%~dp0"
echo =============================================
echo   TELEMETRIAMAPS - COMERCIO EXTERIOR
echo =============================================
echo.
echo Abriendo servidor...
echo Cuando veas "Network URL: http://localhost:8501"
echo ABRE TU NAVEGADOR EN: http://localhost:8501
echo.
echo Para cerrar: cierra esta ventana o Ctrl+C
echo.
python -m streamlit run app/main.py --server.headless false
pause
