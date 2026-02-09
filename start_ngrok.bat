@echo off
echo ========================================
echo   ProSMAT - Demarrage avec ngrok
echo ========================================
echo.

REM Demarrer Django en arriere-plan
echo [1/2] Demarrage du serveur Django...
start "ProSMAT Django Server" cmd /k "cd /d %~dp0 && .\venv_prosmat\Scripts\activate && python manage.py runserver 0.0.0.0:8000"

REM Attendre que Django demarre
echo Attente du demarrage de Django (5 secondes)...
timeout /t 5 /nobreak >nul

REM Demarrer ngrok
echo.
echo [2/2] Demarrage de ngrok...
start "ProSMAT ngrok Tunnel" cmd /k "cd /d %~dp0 && ngrok http 8000"

echo.
echo ========================================
echo   ProSMAT demarre!
echo ========================================
echo.
echo Consultez la fenetre ngrok pour obtenir l'URL publique.
echo Format: https://xxxx-xxxx-xxxx.ngrok-free.app
echo.
echo Identifiants par defaut:
echo   Username: admin
echo   Password: ProSMAT2026!
echo.
echo Appuyez sur une touche pour fermer cette fenetre...
pause >nul
