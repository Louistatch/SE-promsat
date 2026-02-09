@echo off
echo ========================================
echo   ProSMAT - Demarrage avec ngrok
echo ========================================
echo.

REM Arreter les processus existants
echo [0/3] Nettoyage des processus existants...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM ngrok.exe 2>nul
timeout /t 2 /nobreak >nul

REM Demarrer Django en arriere-plan
echo.
echo [1/3] Demarrage du serveur Django...
start "ProSMAT Django Server" cmd /k "cd /d %~dp0 && .\venv_prosmat\Scripts\python.exe manage.py runserver 0.0.0.0:8000"

REM Attendre que Django demarre
echo Attente du demarrage de Django (8 secondes)...
timeout /t 8 /nobreak >nul

REM Demarrer ngrok
echo.
echo [2/3] Demarrage de ngrok...
start "ProSMAT ngrok Tunnel" cmd /k "cd /d %~dp0 && ngrok.exe http 8000"

echo.
echo [3/3] Ouverture du navigateur dans 5 secondes...
timeout /t 5 /nobreak >nul
start http://127.0.0.1:8000

echo.
echo ========================================
echo   ProSMAT demarre!
echo ========================================
echo.
echo IMPORTANT:
echo 1. Consultez la fenetre ngrok (bleue) pour obtenir l'URL publique
echo    Format: https://xxxx-xxxx-xxxx.ngrok-free.app
echo.
echo 2. Copiez cette URL et partagez-la avec votre equipe
echo.
echo 3. Identifiants par defaut:
echo    Username: admin
echo    Password: ProSMAT2026!
echo.
echo 4. Gardez les 2 fenetres ouvertes (Django + ngrok)
echo.
echo Appuyez sur une touche pour fermer cette fenetre...
pause >nul
