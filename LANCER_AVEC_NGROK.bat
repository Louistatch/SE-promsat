@echo off
echo ============================================================
echo DEMARRAGE DE PROSMAT AVEC NGROK
echo ============================================================
echo.

REM Activer l'environnement virtuel
call venv_prosmat\Scripts\activate.bat

echo [1/3] Environnement virtuel active
echo.

REM Démarrer le serveur Django en arrière-plan
echo [2/3] Demarrage du serveur Django sur le port 8000...
start /B python manage.py runserver 8000
timeout /t 3 /nobreak >nul

echo Serveur Django demarre!
echo.

REM Démarrer ngrok
echo [3/3] Demarrage de ngrok...
echo.
echo ============================================================
echo NGROK VA CREER UN TUNNEL PUBLIC
echo ============================================================
echo.
echo Une fois ngrok demarre:
echo 1. Copier l'URL https://xxxxx.ngrok-free.app
echo 2. Ajouter cette URL dans ALLOWED_HOSTS (settings.py)
echo 3. Ajouter cette URL dans Firebase Console (Authorized domains)
echo.
echo Appuyez sur CTRL+C pour arreter ngrok et le serveur
echo.

REM Lancer ngrok
ngrok http 8000

REM Quand ngrok est fermé, arrêter le serveur Django
echo.
echo Arret du serveur Django...
taskkill /F /IM python.exe /T >nul 2>&1

echo.
echo ============================================================
echo APPLICATION ARRETEE
echo ============================================================
pause
