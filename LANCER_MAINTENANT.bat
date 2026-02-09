@echo off
cls
echo.
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo ║                                                                       ║
echo ║                  🚀 LANCEMENT DE PROSMAT 🚀                           ║
echo ║                                                                       ║
echo ╚═══════════════════════════════════════════════════════════════════════╝
echo.

REM Arreter les processus existants
echo [Etape 1/4] Nettoyage...
taskkill /F /IM python.exe 2>nul >nul
taskkill /F /IM ngrok.exe 2>nul >nul
timeout /t 2 /nobreak >nul
echo ✓ Processus nettoyes

REM Demarrer Django
echo.
echo [Etape 2/4] Demarrage de Django...
cd /d %~dp0
start "ProSMAT - Django Server" cmd /k "title ProSMAT Django && color 0A && cd /d %~dp0 && .\venv_prosmat\Scripts\python.exe manage.py runserver 0.0.0.0:8000"
timeout /t 8 /nobreak >nul
echo ✓ Django demarre

REM Demarrer ngrok
echo.
echo [Etape 3/4] Demarrage de ngrok...
start "ProSMAT - ngrok Tunnel" cmd /k "title ProSMAT ngrok && color 0B && cd /d %~dp0 && ngrok.exe http 8000"
timeout /t 5 /nobreak >nul
echo ✓ ngrok demarre

REM Ouvrir le navigateur
echo.
echo [Etape 4/4] Ouverture du navigateur...
start http://127.0.0.1:8000
echo ✓ Navigateur ouvert

echo.
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo ║                                                                       ║
echo ║                  ✅ PROSMAT EST EN LIGNE! ✅                          ║
echo ║                                                                       ║
echo ╚═══════════════════════════════════════════════════════════════════════╝
echo.
echo 📋 PROCHAINES ETAPES:
echo.
echo 1. Dans la fenetre ngrok (bleue), cherchez:
echo    Forwarding    https://xxxx-xxxx.ngrok-free.app
echo.
echo 2. Copiez cette URL
echo.
echo 3. Ouvrez-la dans votre navigateur
echo.
echo 4. Cliquez sur "Visit Site"
echo.
echo 5. Connectez-vous:
echo    Username: admin
echo    Password: ProSMAT2026!
echo.
echo 6. Partagez l'URL avec votre equipe!
echo.
echo ⚠️  IMPORTANT: Gardez les 2 fenetres ouvertes (Django + ngrok)
echo.
echo.
pause
